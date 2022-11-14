n = int(input('Provide the first number to use to compute the collatz sequence: '))

print(f'{n}', end='')

while n != 1:
	# n % 2 is truthy when it's 1, so it's shorter to check
	# for the odd number first
	if n % 2:
		n = 3 * n + 1
	else:
		# floor divison is not necessary as the number is always even,
		# but python will print the number to one decimal place
		#
		# note: we could use {n:.0f} to print to 0 decimal places (i.e. an integer)
		# but it is faster to use floor division
		n //= 2

	print(f', {n}', end='')
