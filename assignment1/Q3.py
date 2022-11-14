from utils import get_next_type

# this is the same as the factorial
# function from the math library
#
# from math import factorial
#
# however, this one is much slower as
# the math library is written in C
def factorial(n: int, /):
	f = 1

	while n:
		f *= n
		n -= 1

	return f

# calculates sin to `terms` terms
def calculate_sin(x: int, terms: int):
	acc = 0

	# implement the infinite sum from the question
	for i in range(terms):
		q = i * 2 + 1
		acc += ((-1) ** i) * ((x ** q) / factorial(q))

	return acc

# calculates cos to `terms` terms
def calculate_cos(x: int, terms: int):
	acc = 0

	# implement the infinite sum from the question
	for i in range(terms):
		q = i * 2
		acc += ((-1) ** i) * ((x ** q) / factorial(q))

	return acc

x = get_next_type('Provide the `x` value to calculate: ', float)
t = get_next_type('Provide the accuracy (terms) to use: ', int, lambda x: x > 0)

# these f-strings (format strings) use the `f` format-specifier,
# {_:f}, which forces _ to display as a float.
#
# this needs to be done to keep parity with the assignment test-case
# as it will force small and large numbers out of scientific notation
print(f'Sin({x}) = {calculate_sin(x, t):.10f}')
print(f'Cos({x}) = {calculate_cos(x, t):.10f}')
