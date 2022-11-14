from enum import Enum
from random import randint
from itertools import count
from dataclasses import dataclass, field
from re import split
from utils import Colour, pluralize, NUM_COLOURS, SPLIT_REGEX

'''
The maximum number guesses allowed by the player.
'''
MAX_GUESSES: int = 15

'''
The maximum number of penalties allowed by the player.
'''
MAX_PENALTIES: int = 5

'''
Exit code when the player wins.
'''
EXIT_SUCCESS = 0

'''
Exit code when the player loses.
'''
EXIT_FAILURE = -1

@dataclass(slots=True)
class Player:
	name: str
	penalties: 'Penalty'
	guesses: int = 0

	def __init__(self, name: str):
		self.name = name
		self.penalties = Penalty(self)

class PenaltyType(Enum):
	REPEAT = 'repeated colors are not allowed in this game'
	VALIDITY = 'cannot recognize the colors you entered'
	NOT_ENOUGH = f'you need to enter at least {NUM_COLOURS} colors for each guess'
	TOO_MANY = f'you need to enter at most {NUM_COLOURS} colors for each guess.'

@dataclass(slots=True)
class Penalty:
	player: 'Player'
	given: set[str] = field(default_factory=set)
	count: int = 0

	def add(self, penalty: 'PenaltyType'):
		self.given.add(penalty.name)

	def process(self):
		'''
		Processes the penalties.

		@returns False if there are no penalties, otherwise True
		'''
		if not self.given:
			return False

		self.count += 1

		# create a raw iterator so the first entry can be processed differently
		# without requiring the logic in every iteration
		penalties = iter(self.given)

		# next() cannot raise an error here because `self.given` has at least one element
		print(f'Sorry {self.player.name}, {PenaltyType[next(penalties)].value}.', end='')

		for name in penalties:
			print(f' Also, {PenaltyType[name].value}.', end='')

		print(' One penalty is considered.')
		print(f'Total penalties = {self.count}')

		# reset the penalty list so it can be re-used
		self.given.clear()

		return True

def prettify_str(string: str) -> str:
	'''
	Converts the first character to upper-case and the
	remaining characters to lower-case.

	```py
	prettify_str('HELLO') # Hello
	```
	'''
	return f'{string[0].upper()}{string[1:].lower()}'

def select_unique_colours(n: int) -> list[Colour]:
	'''
	Selects `n` unique entries from the :ref:`Colour` enum.

	```py
	select_unique_colours(4) # ['RED', 'GREEN', 'BLUE', 'PURPLE']
	```
	'''
	colours = [c.name for c in Colour]

	if n > len(colours):
		raise IndexError(f'`n` can be at most {len(colours)} (received {n=})')

	return [
		Colour[colours.pop(randint(0, len(colours) - 1))]
		for _ in range(n)
	]

def ingest_guess(player: 'Player') -> list[Colour]:
	'''
	Processes and validates the next guess, adding penalties as needed.

	```py
	ingest_guess(Player()) # (0, ['RED', 'BLUE', 'ORANGE', 'SILVER'])
	```
	'''

	# if the player made too many guesses, end the game
	if (player.guesses > MAX_GUESSES):
		print(f'Sorry {player.name}, you ran out of guesses and you lost the game with {player.penalties.count} {pluralize(player.penalties.count, "penalties", "penalty")}.')
		exit(EXIT_FAILURE)

	# get the raw input, stripping whitespace from each side
	raw = input(f'Enter guess number {player.guesses}: ').strip()

	# split the raw input by `\s+` (i.e., one or more spaces)
	guesses = [s.upper() for s in split(SPLIT_REGEX, raw)]
	num_guesses = len(guesses)

	for guess in guesses:
		# did not provide a valid colour
		if guess not in Colour.__members__:
			player.penalties.add(PenaltyType.VALIDITY)
			continue

		# provided a duplicate colour
		if guesses.count(guess) > 1:
			player.penalties.add(PenaltyType.REPEAT)
			continue

	# not enough colours in the guess
	if num_guesses < NUM_COLOURS:
		player.penalties.add(PenaltyType.NOT_ENOUGH)

	# too many colours in the guess
	elif num_guesses > NUM_COLOURS:
		player.penalties.add(PenaltyType.TOO_MANY)

	# True if there was at least penalty
	if player.penalties.process():
		# if there are too many penalties, end the game
		if (player.penalties.count >= MAX_PENALTIES):
			print(f'{player.name}, you lost the game by reaching the maximum number of allowed penalties.')
			exit(EXIT_FAILURE)

		# otherwise, let them guess again
		return ingest_guess(player)

	# if there were no penalties, return the guess
	return [Colour[c] for c in guesses]



def main() -> int:
	# create a random answer of `NUM_COLOURS` unique colours
	answer = select_unique_colours(NUM_COLOURS)

	# This input cannot fail
	name = input('What is your name? ')

	print(f'''Welcome to Master Mind {name}!
The code maker is here. Available colors are
{', '.join(c.value for c in Colour)}
You have {MAX_GUESSES} guesses, total of {MAX_PENALTIES} penalties are allowed but avoid penalties.
The code maker selected {NUM_COLOURS} colors.
You can start guessing {name}.''')

	player = Player(name)

	for index in count(start=1):
		player.guesses = index
		guesses = ingest_guess(player)

		white = NUM_COLOURS
		black = 0

		for i, colour in enumerate(guesses):
			try:
				# list#index raises a ValueError if the value cannot be found
				# in the list. So, if we start `white` at the maximum it can be, we can
				# simply decrement it by 1 if the value is either present and in the correct index
				# or if it doesn't exist at all.
				if i == answer.index(colour):
					white -= 1
					black += 1
			except ValueError:
				white -= 1

		# If all of the colours are in the right position, the player has won
		if black == NUM_COLOURS:
			print(f'''You got {black} {pluralize(black, "blacks", "black", True)} {name}.
You won the game with {player.guesses} {pluralize(player.guesses, "guesses", "guess")} and {player.penalties.count} {pluralize(player.guesses, "penalties", "penalty")}, Congratulations.''')

			return EXIT_SUCCESS

		print(f'You got {black} {pluralize(black, "blacks", "black", True)}, and {white} {pluralize(white, "whites", "white", True)} for this guess.')
	
	return EXIT_FAILURE

if __name__ == '__main__':
	exit(main())
