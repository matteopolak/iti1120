from utils import get_next_type
from dataclasses import dataclass
from math import inf
from random import SystemRandom

# SystemRandom uses os.urandom() under the hood, which
# is cryptographically secure. on the other hand, `random.randint`
# is NOT cryptographically secure. in this case it doesn't matter
# if the number is "truly random" (well, as close as it can be
# with the standard library) because we're only generating a
# handful of numbers.
#
# nonetheless, it's very easy to implement and significantly
# improves the random number generation
generator = SystemRandom()

# create a function that handles playing the game
# and returns the number of guesses it took to win
def play_game(name: str) -> int:
	secret = generator.randint(0, n)
	guesses = 0

	print(f'Starting game for {name}')

	while True:
		guess = get_next_type('Enter your guess: ', int)
		guesses += 1

		if guess < secret:
			print('Too small')
		elif guess > secret:
			print('Too large')
		else:
			print(f'You got it right with {guesses} guess{"" if guesses == 1 else "es"}!')

			return guesses

# `Player` is a class that represents a player
@dataclass(slots=True)
class Player:
	name: str
	guesses: int = 0

	# implement __lt__ so `player1 < player2` can be used
	# this is used when the players are sorted
	def __lt__(self, other: 'Player'):
		return self.guesses < other.guesses

	# implement __str__ so the str built-in can be used on a Player instance
	def __str__(self):
		return self.name

# get the upper bound of the secret number
n = get_next_type('What is the upper limit `n` of the secret number [0, n]? ', int, lambda x: x > -1)


# get the number of players
p = get_next_type('How many players are in the game? ', int, lambda x: x > -1)

# question says `p` is a positive integer, so we must handle
# the case where it is 0
if p == 0:
	print('No players entered the game, so there are no winners.')

	exit()

# a list of players with the fewest guesses
winners: list[Player] = []

# the number of guesses it took the winner(s)
# start at inf (infinity) so the first player has the fewest
winner_guess = inf

for i in range(p):
	name = input(f'What is your name Player {i + 1}? ')
	guesses = play_game(name)

	# if the player ties, add them to the winners list
	if guesses == winner_guess:
		winners.append(Player(name, guesses))
	# if they have the fewest guesses, update the guess count,
	# clear the winner list, and add the current player
	elif guesses < winner_guess:
		winner_guess = guesses
		winners.clear()
		winners.append(Player(name, guesses))

# finally, print the names of the winners (joined by commas)
# followed by `are the winners` if there are multiple, or `is the winner`
# if there is only one
print(', '.join(map(str, winners)), 'are winners.' if len(winners) > 1 else 'is the winner.')
