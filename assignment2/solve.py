from itertools import permutations
from math import inf
from re import split
from utils import Colour, pluralize, NUM_COLOURS, SPLIT_REGEX
from multiprocessing import Pool, cpu_count

'''
True if the user provides the number of blacks and whites
'''
MANUAL_INPUT = True

'''
Must be present if :ref:`MANUAL_INPUT` is True
'''
ANSWER = [Colour.BLUE, Colour.ORANGE, Colour.CYAN, Colour.TEAL]

def submit(guess: tuple[Colour, ...]) -> tuple[int, int]:
	'''
	Provides a guess and formats the response. This does *not* handle
	invalid input and *will* crash.

	@returns A tuple of (black, white)
	'''

	# if the MANUAL_INPUT flag is set, let the user choose
	if MANUAL_INPUT:
		return map(
			int,
			split(
				SPLIT_REGEX,
				input(f'{" ".join(c.value for c in guess)}: ').strip(),
				2
			)
		)

	print(f'Guess given: {" ".join(c.value for c in guess)}')

	c_black = c_white = 0

	for i, c in enumerate(guess):
		if c == ANSWER[i]:
			c_black += 1
		elif c in ANSWER:
			c_white += 1

	return c_black, c_white

def calculate_min_score(
	possible: tuple[Colour, ...],
	answers: set[tuple[Colour, ...]],
	responses: list[tuple[int, int]]
):
	'''
	Calculates the minimum number of answers that will be eliminated
	if `possible` is the next guess chosen.
	'''

	# start with infinity as any number will be able to
	# overwrite it
	min_score = inf

	# iterate through every possible response
	for black, white in responses:
		# keep track of the number of eliminations
		score = 0

		# iterate through each code
		for code in answers:
			c_black = c_white = 0

			# iterate through each colour in the code
			for i, c in enumerate(code):
				# same as before, it's black if the colours at the same index
				# are equal
				if c == possible[i]:
					c_black += 1

					if c_black > black:
						break
				elif c in possible:
					c_white += 1

					if c_white > white:
						break

			if c_black != black or c_white != white:
				score += 1

		# if the current score is less than the smallest score,
		# replace the smallest score
		if score < min_score:
			min_score = score

	# finally, return a tuple with the smallest score and the
	# code tested (so we can sort them by min_score)
	return min_score, possible

def main(pool: Pool):
	'''
	There are only 5,040 answers, 10P4 (assuming NUM_COLOURS=4)

	Strategy:
	Start with any 4 colours and get the number of blacks and whites.

	For every remaining possible solution, test them against the guess and eliminate
	them if they do not give the same answer as the one provided for the guess.

	The next guess will be the guess that eliminates the most possible solutions
	in the worst-case scenario (i.e. compute the minimum number of solutions eliminated
	for every possible answer, and pick the guess with the highest minimum eliminations).
	If there is more than one next best guess, pick any best guess that is also a possible answer.
	If no best guess is also a possible answer, pick any best guess.
	'''

	# print out the instructions if the MANUAL_INPUT flag is enabled
	if MANUAL_INPUT:
		print(f'''Available colours: {' '.join(c.value for c in Colour)}

As a response to each guess, use two integers separated by a space where
the first integer is the number of blacks, and the second is the number of whites.

For example, this would be 3 blacks and 1 white:
3 1
''')

	# compute every possible answer
	possibilites = set(permutations(Colour, NUM_COLOURS))

	# copy the set since we'll be removing impossible answers
	# from it (we don't want it to affect the possible guesses)
	answers = possibilites.copy()

	# keep track of the number of guesses
	guess_count = 0

	# compute all possible responses
	responses = [
		(i, j)
		for i in range(NUM_COLOURS + 1)
		for j in range(NUM_COLOURS - i + 1)
	]

	# the first guess is random
	guess = answers.pop()

	while True:
		black, white = submit(guess)
		guess_count += 1

		if black == NUM_COLOURS:
			break

		# ensure the same guess isn't made twice
		possibilites.remove(guess)

		# remove impossible answers
		for code in answers.copy():
			c_black = c_white = 0

			for i, c in enumerate(code):
				# if the code at the current index is equal to the code at
				# the same index in the guess, add one to the black counter
				if c == guess[i]:
					c_black += 1

					# if the black counter is greater than the required black
					# count, we can safely skip the rest
					if c_black > black:
						break
				# otherwise, if the colour is somewhere in the guess
				# then add one to the white counter
				elif c in guess:
					c_white += 1

					if c_white > white:
						break

			# if the counters are not exactly equal, it's impossible
			# for it to be an answer so we can remove it
			if c_black != black or c_white != white:
				answers.remove(code)

		# get the answer count and store it in a variable to avoid
		# calling it three times (since we need it multiple times)
		answers_count = len(answers)

		# print out a nice message to the ui
		print(f'Computing the next guess. This may take a while... ({answers_count} {pluralize(answers_count, "answers", "answer")} remaining)')

		if answers_count > 1:
			# calculate the min score for every possibility (including answers that
			# are impossible) using multiprocessing as it takes a while with a single
			# process
			results: list[tuple[float | int, tuple[Colour, ...]]] = pool.starmap(
				calculate_min_score,
				((p, answers, responses) for p in possibilites)
			)

			# get the highest score
			highest = max(results, key=lambda x: x[0])[0]

			# get a list of all colour sets with the highest score
			highest_set = set(map(lambda x: x[1], filter(lambda x: x[0] == highest, results)))

			# get all guesses that are also a possible answer
			guesses_in_answers = answers & highest_set

			# if there is one, use it
			if guesses_in_answers:
				guess = guesses_in_answers.pop()
			# otherwise just use any guess
			else:
				guess = highest_set.pop()
		else:
			# since there is only one possibility left, it must be the answer
			guess = answers.pop()

	print(f'Yay, finished the game in {guess_count} {pluralize(guess_count, "guesses", "guess")}!')

# required when using multiprocessing, as each spawned process
# will load `play.py` and we don't want it to run everything that
# the main process does
if __name__ == '__main__':
	with Pool(cpu_count()) as pool:
		main(pool)
