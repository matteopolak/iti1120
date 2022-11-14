from random import randint

n = int(input('Provide the upper bound `n` for [0, n]: '))

def start_game():
	# get a random number from [0, n]
	secret = randint(0, n)

	print('Starting the game')

	# create an infinite loop that exits on victory
	while True:
		guess = int(input(f'Enter your guess: '))

		if guess < secret:
			print('Too small')
		elif guess > secret:
			print('Too large')
		else:
			print('You guessed it right!')

			break

while True:
	start_game()

	# y, Y, and [blank] will continue playing
	play_again = input('Would you like to play again? [Y/n] ')

	if play_again != '' and play_again.lower() != 'y':
		break
