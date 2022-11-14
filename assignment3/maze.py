# Matthew Polak 300286703

from queue import PriorityQueue
from dataclasses import dataclass, field
from math import inf
from typing import Union
from structs import Grid, MazeError, Node, NodeType, Option, Path

@dataclass(slots=True)
class MazeSolver:
	maze: 'Maze'
	start: 'Node'
	end: 'Node'
	nodes: set['Node']

	remaining: PriorityQueue[tuple[float, 'Node']] = field(init=False)
	r_score: dict['Node', float] = field(default_factory=dict)
	h_score: dict['Node', float] = field(default_factory=dict)

	def solve(self) -> Union['Path', None]:
		'''
		Solves the path using A*
		'''
		# r_score is the raw score (i.e., the cheapest path to the origin)
		self.r_score = { node: inf for node in self.nodes }
		self.r_score[self.start] = 0

		path = Path(self.start, self.end)

		self.h_score = self.r_score.copy()
		self.h_score[self.start] = self.start.heuristic(self.end)

		# create a priority queue
		#
		# this is not really needed, a list would be fine and
		# would still be O(n) for getting the smallest value
		#
		# however, a priority queue (more specifically, a min-heap
		# in this case) is O(log n)
		self.remaining = PriorityQueue()

		# add the start node
		self.remaining.put((self.h_score[self.start], self.start))

		# while there are still nodes to explore...
		while self.remaining.qsize() != 0:
			# get the node with the lowest r_score, or the node with the
			# shortest path to the origin
			_, node = self.remaining.get_nowait()

			# if the closest node is the end, we've found the shortest path
			if node == self.end:
				return path

			# then, iterate through all of the neighbour nodes, which
			# were built with `make_node`
			for neighbour in node.neighbours:
				# get the would-be score by adding the cost between
				# the neighbour and the current node (which is always
				# going to be 1 in this problem)
				score = self.r_score[node] + 1

				# if the score is lower than its current score
				if score < self.r_score[neighbour]:
					# set the path from the node to the neighbour
					#
					# you can read this as:
					# 'the shortest path to `neighbour` is from `node`'
					path.add_node(node, neighbour)

					# then, update the r_score with the new (and lower) score
					self.r_score[neighbour] = score

					# and the h_score with the sum of the new score and the heuristic
					# computation (which is just the absolute difference from the end)
					self.h_score[neighbour] = score + neighbour.heuristic(self.end)

					# finally, let the neighbour be explored
					# note: this will *never* result in `self.remaining` having
					# the same node added more than once, since `r_score` must be
					# strictly lower than the current r_score
					self.remaining.put_nowait((self.h_score[neighbour], neighbour))

		# if we reach this, the two points do not have a path
		return None

@dataclass(slots=True)
class Maze:
	grid: Grid
	start: Node = field(default_factory=Node)
	end: Node = field(default_factory=Node)
	remaining: set['Node'] = field(default_factory=set)
	all: set['Node'] = field(default_factory=set)

	@staticmethod
	def from_rows(rows: list[str]) -> 'Maze':
		grid = [list(map(lambda c: Node.from_char(c[1], c[0], y), enumerate(row))) for y, row in enumerate(rows)]
		maze = Maze(grid)

		start = None
		end = None

		for row in maze.grid:
			if row[0].type != NodeType.WALL:
				start = row[0]

				if end is not None:
					break
			elif row[-1].type != NodeType.WALL:
				end = row[-1]

				if start is not None:
					break

		if start is None or end is None:
			raise MazeError('maze does not have an entrance and exit')

		maze.start = start
		maze.end = end

		# attach the nodes
		maze.add_node(start)

		return maze

	def get_node(self, x: int, y: int) -> Option['Node']:
		try:
			return self.grid[y][x]
		except IndexError:
			return None

	def get_path_between(self, start: 'Node', end: 'Node'):
		solver = MazeSolver(self, start, end, self.all)

		return solver.solve()

	def find_node_by_type(self, n_type: 'NodeType') -> Option['Node']:
		for row in self.grid:
			for node in row:
				if node.type == n_type:
					return node
		
		raise MazeError(f'no node found with type {n_type}')

	def add_node(self, node: 'Node'):
		self.all.add(node)

		neighbours = (
			# up
			self.get_node(node.point.x, node.point.y - 1),
			# down
			self.get_node(node.point.x, node.point.y + 1),
			# left
			self.get_node(node.point.x - 1, node.point.y),
			# right
			self.get_node(node.point.x + 1, node.point.y)
		)

		# store the neighbours that should be explored
		# we explore *after* updating all neighbours of the current
		# node to avoid infinite recursion
		explore: list['Node'] = []

		for neighbour in neighbours:
			# if it's not a wall and it's not already a neighbour, add it
			if neighbour is not None and neighbour.type != NodeType.WALL and neighbour not in node.neighbours:
				# add mutual neighbours
				node.neighbours.add(neighbour)
				neighbour.neighbours.add(node)

				# add the node to the explore list
				explore.append(neighbour)

		# explore each node in the `explore` list
		#
		# note: this *will* raise an error if number of valid path nodes
		# is too large, as Python has a recursion limit of 1,000.
		# if you're reading this and want to try out a MASSIVE maze,
		# increase the recursion limit with the following:
		#
		# ```py
		# import sys
		#
		# sys.setrecursionlimit(10_000)
		# ```
		for node in explore:
			self.add_node(node)
