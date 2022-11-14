'''
note: not allowed to use log10, so this is technically faster
			as the alternative requires iterating over the digits
			to count them anyway

for example:

def count_digits(number: int):
	return floor(log10(number)) + 1

def get_first_n(number: int, n: int):
	return number // (10 ** (count_digits(number) - n))
'''
def starts_with_n(number: int, n: int):
	if not n and number:
		return False

	while number:
		if number == n:
			return True

		number //= 10

	return False

n = int(input('Provide the value for `n`: '))
k = int(input('Provide the value for `k`: '))

starts_with_k = []

for i in range(1, n + 1):
	number = int(input(f'Provide number #{i}: '))

	if starts_with_n(number, k):
		'''
		note: question speficially states
					'You are not allowed to use strings in this program'

		this number is being converted into a string in order to print it
		'''
		starts_with_k.append(str(number))

print(*starts_with_k)
