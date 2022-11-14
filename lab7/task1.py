from typing import TypeVar
from utils import get_next_type

N = TypeVar('N', int, float)

def get_next_set(title: str) -> set[float]:
	# `n` is the number of elements that will be provided to add to the set
	#
	# note: this is not necessarily going to be the number of elements
	#       in the set as they may not all be unique
	n = get_next_type(f'Provide the number of elements for set {title}: ', int, lambda x: x > -1)

	# iterate `n` times -- [1, n] so i can use `i` instead of `i + 1` when printing
	# (since `i` isn't used for anything else besides the tui)
	return {
		get_next_type(f'Provide element {i} for set {title}: ', float)
		for i in range(1, n + 1)
	}

# sorts entries, removes trailing zeros, joins with commas,
# and places curly braces around result
def pretty_format_set(s: set[N]) -> str:
	return f'{{{", ".join(map(lambda x: format(x, "g"), sorted(s)))}}}'

# get all sets
u = get_next_set('U')
a = get_next_set('A')
b = get_next_set('B')

# print out info
print(f'A Union B = {pretty_format_set(a | b)}')
print(f'A Intersection B = {pretty_format_set(a & b)}')
print(f'A - B = {pretty_format_set(a - b)}')
print(f'B - A = {pretty_format_set(b - a)}')
print(f'A Complement = {pretty_format_set(u - a)}')
print(f'B Complement = {pretty_format_set(u - b)}')
print(f'A ^ B = {pretty_format_set(a ^ b)}')

# cache results because we use both at least once
a_sub_b = a <= b
b_sub_a = b <= a

if a_sub_b and b_sub_a:
	print('A is equal to B')
elif a_sub_b:
	print('A is a subset of B')
elif b_sub_a:
	print('B is a subset of A')
else:
	print('A is not a subset of B, B is not a subset of A')
