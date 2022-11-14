from dataclasses import dataclass

@dataclass(slots=True)
class SquareMatrix():
	rows: list[list[float]]
	n: int

	def __init__(self, n: int):
		self.n = n

		# create a zero matrix
		self.rows = [
			[0 for _ in range(n)]
			for _ in range(n)
		]

	def is_lower_triangular(self) -> bool:
		return all(
			map(
				lambda e: all(
					map(
						lambda x: x == 0,
						e[1][e[0] + 1:]
					)
				),
				enumerate(self.rows[:-1])
			)
		)

	def is_upper_triangular(self) -> bool:
		return all(
			map(
				lambda e: all(
					map(
						lambda x: x == 0,
						e[1][:e[0] + 1]
					)
				),
				enumerate(self.rows[1:])
			)
		)

	def set_data(self, row: int, col: int, data: float):
		self.rows[row][col] = data

def get_next_matrix(title: str):
	n = int(input(f'Provide the number of rows/columns for matrix {title}: '), base=10)
	m = SquareMatrix(n)

	for i in range(n):
		for j in range(n):
			m.set_data(i, j, float(input(f'Provide the number for row {i + 1} and column {j + 1} for matrix {title}: ')))

	return m

m = get_next_matrix('A')

upper = m.is_upper_triangular()
lower = m.is_lower_triangular()

if upper and lower:
	print('This matrix is both lower and upper triangular.')
elif upper:
	print('This matrix is upper triangular.')
elif lower:
	print('This matrix is lower triangular.')
else:
	print('This matrix is neither upper nor lower triangular.')
