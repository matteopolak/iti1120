# Matthew Polak 300286703

from maze import Maze
from structs import NodeType, PathError
from utils import print_maze_with_path, raw_grid_from_rows

def solve_maze(rows: list[str], *, with_s: bool = True):
	maze = Maze.from_rows(rows)

	if with_s:
		s_node = maze.find_node_by_type(NodeType.ROCKET)

		# theoretically should never happen because the question states
		# the rocket is always present, but check it anyway
		if s_node is None:
			raise PathError("rocket not found in maze")
	else:
		s_node = maze.end

	path_to_s = maze.get_path_between(maze.start, s_node)

	# if the start and end point are the same, don't search
	# for the path from the rocket to the end
	#
	# this will either happen when `with_s` is False, or when
	# the rocket is also the exit
	if s_node == maze.end:
		if path_to_s is None:
			raise PathError("no path found from start to end")

		return path_to_s.collect()

	if path_to_s is None:
		raise PathError("no path found to rocket")

	path_to_end = maze.get_path_between(s_node, maze.end)

	if path_to_end is None:
		raise PathError("no path found from rocket to end")

	return path_to_s.append(path_to_end)

def main(rows: list[str]):
	path = solve_maze(rows, with_s=False)
	raw_grid = raw_grid_from_rows(rows)

	# print out the path with stars
	print_maze_with_path(raw_grid, path, False)
	print()

	# print out the path with directions added
	#
	# note: we can re-use the same raw grid because we're
	# overwriting all of the points that were written to in the
	# previous `print_maze_with_path` function call since we
	# use the same path
	print_maze_with_path(raw_grid, path, True)
	print(f'Length of the minimum path = {len(path)}')
	print()

	path = solve_maze(rows, with_s=True)

	# print out the raw path with the rocket included
	print(path)

if __name__ == '__main__':
	# use a string for the grid instead of manually creating the array.
	# note: we need to slice the first and last characters as they are both \n
	# then call str#splitlines to split it into lines, or str#split if you
	# know which format it will be (i.e. usually CRLF for windows-based, LF for
	# darwin/linux-based)
	main('''
################
#ppppp#pps##pp##
pp###pppp###pp##
#p###pp#p##ppp##
#pppp##pp##ppp##
####p###########
###pp###########
####ppppp#######
########pp####pp
########ppppppp#
################
'''[1:-1].splitlines())
