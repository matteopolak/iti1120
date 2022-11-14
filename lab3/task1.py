from math import sqrt, floor

# not the fastest, but good enough
def is_prime(n: int):
	if n <= 1:
		return False

	for i in range(2, floor(sqrt(n)) + 1):
		if n % i == 0:
			return False

	return True

prime_count = 0
messages = (
	'Provide the first bound: ',
	'Provide the second bound: ',
)

'''
since the question does not state that the bounds are provided
in a specific order (i.e. ascending or descending), sort them
so a <= b
'''
a, b = sorted(int(input(messages[i])) for i in range(2))

print('Primes = ', end='')

for n in range(a, b + 1):
	if is_prime(n):
		prime_count += 1

		print(f'{n} ', end='')

print(f'\nNumber of Primes = {prime_count}')
