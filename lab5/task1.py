from math import sqrt, floor

def get_divisors(n: int):
	if n == 0:
		return
	
	yield 1

	for i in range(2, floor(sqrt(n)) + 1):
		if n % i == 0:
			yield i
			yield n // i

def is_complete(n: int):
	return sum(get_divisors(n)) == n

n = int(input('Provide an integer to check for complete-ness: '))
c = is_complete(n)

print(f'{n} is{"" if c else " not"} a complete number.')
