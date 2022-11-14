from utils import get_next_type
from math import sqrt, floor

n = get_next_type('Provide an integer greater than 1: ', int, lambda x: x > 1)

# get the smallest factor
def get_factor(n: int):
	for i in range(2, floor(sqrt(n)) + 1):
		if n % i == 0:
			return i

	return None

# add a factor to the dictionary, or increment
# that factor's count if it already exists
#
# this can also be accomplished with a defaultdict,
# but it's easy enough to implement that the extra
# library seems pointless
def add_factor(f: int, factors: dict[int, int]):
	if f in factors:
		factors[f] += 1
	else:
		factors[f] = 1

# get all prime factors
# we know they're all prime because `n` will continue to
# be divided into its smallest parts until it is 0
def get_prime_factors(n: int):
	# create a dictionary to hold the number of each factor
	factors: dict[int, int] = {}

	# equivalent to `while n != 0`
	while n:
		# get `f`, the smallest factor of `n`
		f = get_factor(n)

		# if there is no factor, `n` is prime
		# therefore, add `n` to the factors and exit
		if f is None:
			add_factor(n, factors)

			break

		# otherwise, divide `n` by `f` 
		n //= f

		# and add `f` to the list of factors
		add_factor(f, factors)

	# return the factory dict
	return factors

# formats the factor dict into a string
def format_factor_dict(factors: dict[int, int]):
	# create a list to append the formatted text
	# this is significantly more performant than
	# concatenating strings
	items: list[str] = []

	# dict#items returns a view on the dictionary entries,
	# returning an iterator of (key, value)
	for k, v in factors.items():
		# if the count of the factor is greater than 1,
		# raise it to the `v` power
		if v > 1:
			items.append(f'{k}^{v}')
		# otherwise, just append it normally
		else:
			items.append(f'{k}')

	return items

# print out the left-hand side:
# "{input number} = "
print(f'{n} = ', end='')

# this is shorthand for the following:
# print(' * '.join(format_factor_dict(get_prime_factors(n))))
#
# personally, it looks more readable with the spread operator
print(*format_factor_dict(get_prime_factors(n)), sep=' * ')
