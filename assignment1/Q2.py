from utils import get_next_type
from string import digits, ascii_letters

number = get_next_type('Provide the integer to convert: ', int)
base = get_next_type('Provide the base to convert to: ', int)

# digits, lowercase, uppercase, +, /
dictionary = [*digits, *ascii_letters, '+', '/']

# note: this will NOT give the same version of bases > 16 as is convention.
#       in practice, base-64 is: uppercase, lowercase, numbers, +, /.
#       however, i would like digits to go first and followed by lowercase
#       characters to work correctly up to base-16.
def get_digit_representation(n: int):
	return dictionary[n]

# get the sign of the number, since converting a number from
# one base to another retains the same sign
sign = '-' if number < 0 else ''

# make sure `number` is positive
number = abs(number)

# create an array to store each digit in the converted base
parts: list[str] = []

# create a counter to create the converted digit
# without the use of strings
total = 0

# shorthand for `while number != 0`
while number:
	# get the remainder of the number divided by the base
	# this will be the next digit in the converted base
	remainder = number % base

	# remove the used parts of the original number
	number //= base

	# add the new digit to the `parts` array
	parts.append(get_digit_representation(remainder))

# `parts` is actually the new number in reverse order
#
# ... which is exactly what we want!
#
# to convert it into something we can print, it
# must be a string since Python does not support
# arbitrary bases in print formatting :(
#
# so... let's reverse the list and join it into a string
# and apply the sign from the beginning (- if negative,
# nothing if >= 0)
print(f'{sign}{"".join(reversed(parts))}')
