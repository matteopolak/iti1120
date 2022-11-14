n = int(input('Enter the number of rows: '), base=10)

puzzle: list[str] = [
    input(f'Enter row number {i} of the puzzle: ') for i in range(1, n + 1)
]

word = input('Enter the word to search for: ')

rows = len(puzzle)
cols = len(puzzle[0])

def transform(title: str, row: int, col: int, hori: bool, vert: bool,
              diag: bool):
	col_t = cols - col if hori else col + 1
	row_t = rows - row if vert else row + 1

	if diag:
		direction = f'{" up" if vert else " down"}{" left" if hori else " right"}'
	else:
		direction = ' reverse' if vert or hori else ''

	return f'{word} is at row {row_t} and column {col_t} {title}{direction}.'

def find_word(word: str,
              puzzle: list[str],
              *,
              hori: bool = False,
              vert: bool = False):
	word_len = len(word)

	# horizontal
	for i, row in enumerate(puzzle):
		index = row.find(word)

		if index != -1:
			print(transform('horizontal', i, index, hori, vert, False))
			exit(0)

	# vertical
	for i, col in enumerate(map(''.join, zip(*puzzle))):
		index = col.find(word)

		if index != -1:
			print(transform('vertical', index, i, hori, vert, False))
			exit(0)

	# diagonal left side
	for i in range(0, rows - word_len + 1):
		dia = ''.join(puzzle[i + j][j] for j in range(min(rows, cols - i)))
		index = dia.find(word)

		if index != -1:
			print(transform('diagonal', i + index, index, hori, vert, True))
			exit(0)

	# diagonal top
	for i in range(1, cols - word_len + 1):
		dia = ''.join(puzzle[j][i + j] for j in range(min(cols, rows - i)))
		index = dia.find(word)

		if index != -1:
			print(transform('diagonal', index, i + index, hori, vert, True))
			exit(0)

# regular
find_word(word, puzzle)

# flipped vert
puzzle.reverse()
find_word(word, puzzle, vert=True)

# flipped vert + hori
puzzle = list(map(lambda r: r[::-1], puzzle))
find_word(word, puzzle, hori=True, vert=True)

# flipped hori
puzzle.reverse()
find_word(word, puzzle, hori=True)
