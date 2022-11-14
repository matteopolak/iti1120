from utils import get_next_type
from dataclasses import dataclass, field

@dataclass(slots=True)
class Set:
	data: list[float] = field(default_factory=list)

	# this method is private (by convention)
	# and just returns the opposite of Set#contains
	# to make the filter in the operations a bit cleaner
	def __not_contains(self, value: float):
		return not self.contains(value)

	def add(self, value: float):
		# O(N) because i can't use a dict() or set()
		if value not in self.data:
			self.data.append(value)

	def remove(self, value: float):
		# check if the value exists before removing it
		#
		# note: this check is required because Python
		#       will raise a ValueError if it doesn't exist
		#       when attempting to remove it
		if value in self.data:
			# if it exists, remove it
			self.data.remove(value)

	# returns True if the value exists in the set
	def contains(self, value: float):
		return value in self.data

	# implement the iter method by returning
	# the data (since it's already an iterator)
	def __iter__(self):
		return iter(self.data)

	# implement the repr method which is called
	# by the print built-in to display the class
	def __repr__(self):
		# sort the numbers in ascending order. this is to keep
		# parity with the answer in the assignment
		#
		# then, strip trailing zeros and periods if the number
		# is a decimal; once again this is done to keep parity
		# with the answer in the assignment
		tokens = map(lambda s: s.rstrip('0.') if '.' in s else s, map(str, sorted(self)))

		# finally, join the tokens with commas and wrap
		# them in curly braces
		#
		# note: double braces escapes the braces entirely,
		#       so you need three to have it actually show a brace
		return f'{{{", ".join(tokens)}}}'

	# the rest of this class is to implement the set operations
	#
	# note: `a` is `self` in all of the below methods
	#       and a trailing slash is appended to the end of
	#       the parameter list to indicate that the name of
	#       parameter `b` does not hold any external value

	# implement A ^ B
	def __xor__(a, b: 'Set', /):
		disjunct = Set()

		for k in filter(b.__not_contains, a):
			disjunct.add(k)

		for k in filter(a.__not_contains, b):
			disjunct.add(k)

		return disjunct

	# implement A - B
	def __sub__(a, b: 'Set', /):
		sub = Set()

		for k in filter(b.__not_contains, a):
			sub.add(k)

		return sub

	# implement A & B
	def __and__(a, b: 'Set', /):
		intersect = Set()

		for k in filter(b.contains, a):
			intersect.add(k)

		for k in filter(a.contains, b):
			intersect.add(k)

		return intersect

	# implement A | B
	def __or__(a, b: 'Set', /):
		union = Set()

		for k in a:
			union.add(k)

		for k in b:
			union.add(k)

		return union

def get_next_set(index: int):
	# `n` is the number of elements that will be provided to add to the set
	#
	# note: this is not necessarily going to be the number of elements
	#       in the set as they may not all be unique
	n = get_next_type('Provide the number of elements in the next set: ', int, lambda x: x > -1)

	# create a new set
	s = Set()

	# iterate `n` times -- [1, n] so i can use `i` instead of `i + 1` when printing
	# (since `i` isn't used for anything else besides the tui)
	for i in range(1, n + 1):
		d = get_next_type(f'Provide element {i} for set {index}: ', float)

		# add the new element to the set
		s.add(d)

	return s

# `u` is the universal set. the question states (a | b) & u = u
#     (i.e. a and b are contained in u)
#
# a and b are arbitrary sets
u, a, b = [get_next_set(i) for i in range(1, 4)]

# since we implemented __or__, __and__, __sub__, and __xor__,
# we can use the operations in the exact same way as the built-in `set`
#
# note: the `Set` implementation above is a drop-in replacement if these
#       are the only methods you need to use (i.e., replacing `Set` with `set`
#       in `get_next_set` will return the same answers)
print(f'A Union B = {a | b}')
print(f'A Intersection B = {a & b}')
print(f'A – B = {a - b}')
print(f'B – A = {b - a}')
print(f'A Complement = {u - a}')
print(f'B Complement = {u - b}')
print(f'A ^ B = {a ^ b}')
