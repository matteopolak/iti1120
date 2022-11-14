n = int(input('Provide a positive integer: '))

# create a generator that iterates over all numbers <= n
# and filter out numbers that arent a divisor (i.e. whose mod with n isn't 0)
divisors = (i for i in range(2, n + 1) if n % i == 0)
total = 1

print('Divisors = 1', end='')

for divisor in divisors:
	total += divisor

	print(f', {divisor}', end='')

print(f'\nSum of divisors = {total}')
