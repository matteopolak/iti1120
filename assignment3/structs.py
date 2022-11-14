# Matthew Polak 300286703

from dataclasses import dataclass, field
from enum import Enum
from typing import TypeAlias, TypeVar

T = TypeVar('T')

# inspired by https://doc.rust-lang.org/std/option/enum.Option.html
Option: TypeAlias = T | None

# utility types to keep track of everything
# without using potentially confusing list structures
PrettyPath: TypeAlias = list['Node']
Grid: TypeAlias = list[list['Node']]
RawGrid: TypeAlias = list[list[str]]

class PathError(Exception):
	pass

class MazeError(Exception):
	pass

class NodeType(Enum):
	WALL = 0
	PATH = 1
	ROCKET = 2

	@staticmethod
	def from_char(char: str):
		match char:
			case '#':
				return NodeType.WALL
			case 'p':
				return NodeType.PATH
			case 's':
				return NodeType.ROCKET
			case _:
				raise PathError(f'unknown path node "{char}"')

@dataclass(slots=True, frozen=True, unsafe_hash=True, order=True)
class Point:
	# coordinates are `int`s because they represent
	# boxes on the maze, which are always whole numbers
	x: int
	y: int

	# override the repr to display the same output as the
	# output in the assignment: (y + 1, x + 1)
	def __repr__(self):
		return f'({self.y + 1}, {self.x + 1})'

	@staticmethod
	def from_node(node: 'Node'):
		# return a reference to the point since
		# we assume it's always frozen
		return node.point

@dataclass(slots=True)
class Node:
	point: 'Point' = field(default=Point(0, 0))
	type: 'NodeType' = NodeType.WALL
	neighbours: set['Node'] = field(default_factory=set)

	@staticmethod
	def from_char(char: str, x: int, y: int):
		return Node(Point(x, y), NodeType.from_char(char))

	# see: https://xlinux.nist.gov/dads/HTML/manhattanDistance.html
	def heuristic(self, end: 'Node') -> float:
		return abs(self.point.x - end.point.x) + abs(self.point.y + end.point.y)

	# two nodes are the same if their position is equal
	def __hash__(self):
		return hash(self.point)

	# print out the Point's repr when getting the repr of the Node
	def __repr__(self):
		return repr(self.point)

	# we need to implement __lt__ so `Node` can be used in the tuple
	# stored in the priority queue
	#
	# however, we don't care about the accuracy of `Node` ordering since they
	# only need to be ordered by their h_score. therefore, we just return True
	# every time because it doesn't matter
	def __lt__(self, _: 'Node'):
		return True

@dataclass(slots=True)
class Path:
	__end: 'Node'
	__start: 'Node'
	__path: dict['Node', 'Node']

	def __init__(self, start: 'Node', end: 'Node'):
		self.__start = start
		self.__end = end
		self.__path = {}

	def add_node(self, s: 'Node', e: 'Node'):
		self.__path[e] = s

	def collect(self) -> PrettyPath:
		'''
		Collects the path into a list of `Node`s,
		where path[n+1] is the next node in the path
		from path[n]
		'''
		rev_path: PrettyPath = []
		next = self.__end

		while next:
			rev_path.append(next)
			next = self.__path.get(next, None)

		rev_path.reverse()

		return rev_path

	def append(self, other: 'Path') -> PrettyPath:
		'''
		Merges two paths, removing the redundant starting node
		from the second path
		'''
		if other.__start != self.__end:
			raise PathError('`self` does not share endpoints with `other`')

		path = self.collect()
		path.extend(other.collect()[1:])

		return path
