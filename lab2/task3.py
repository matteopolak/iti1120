n = int(input('Provide a non-negative integer: '))
rev = 0

while n > 0:
	# extract the last digit by using modulo 10
	# this works because the unit is the only portion <10
	d = n % 10

	# use floor divison (equivalent to `n = floor(n / 10)`)
	# to "shift" the number to the right
	n //= 10

	# multiply the current reversed number by 10 (shifting all digits to the left)
	# then add the current digit
	rev *= 10
	rev += d

print(f'{rev}')
