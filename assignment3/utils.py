# Matthew Polak 300286703

from structs import Node, Option, PathError, PrettyPath, RawGrid

def raw_grid_from_rows(rows: list[str]) -> RawGrid:
	return list(map(list, rows))

def get_direction(node: 'Node', next: Option['Node']):
	if next is None:
		return '>'
	
	delta_x = next.point.x - node.point.x

	if delta_x == -1:
		return '<'
	elif delta_x == 1:
		return '>'

	delta_y = next.point.y - node.point.y

	if delta_y == -1:
		return '^'
	elif delta_y == 1:
		return 'v'

	raise PathError(f'node {node} does not move anywhere ({next=}')

def print_maze_with_path(grid: RawGrid, path: PrettyPath, with_dir: bool):
	path_len = len(path)

	if with_dir:
		for i, node in enumerate(path):
			# get the next node in the path
			next_node = path[i + 1] if i + 1 < path_len else None
			direction = get_direction(node, next_node)

			# overwrite the grid point with the new direction
			grid[node.point.y][node.point.x] = direction
	else:
		for node in path:
			# if no direction is needed, overwrite the grid with a star
			grid[node.point.y][node.point.x] = '*'
	
	# finally, print out the grid
	print(*map(''.join, grid), sep='\n')
