from utils import get_next_type
from dataclasses import dataclass, field

# use a dataclass because it saves on boilerplate.
# the `slots` option will improve the memory usage and
# access speed of all attributes
#
# it works by inlining the attributes as opposed to
# allowing dynamic keys with the __dict__ it normally uses
@dataclass(slots=True)
class Pascal:
	# `row` is the current row
	row: list[int] = field(default_factory=list)
	# `row_number` is the current row number
	row_number: int = 0

	# __iter__ is called when a new iterator is created on the class
	#
	# note: since this is mutating itself and returning itself
	#       it WILL affect the current iterator if __iter__ is called
	#       while it's already iterating. however, it doesn't matter in
	#       this case because it is only called once
	def __iter__(self):
		self.row = []
		self.row_number = -2

		return self

	# __next__ is called when the next item from the iterator is needed
	#
	# note: this mutates the same row that is returned so it is assumed
	#       that the array is NOT mutated outside of the class.
	#       not worth the effort to enforce this in Python, but it is
	#       one of the concerns with this.
	#
	#       of course, i could just return a copy of the row, but i know
	#       it isn't being mutated so it isn't worth the loss of performance
	#       and memory usage
	def __next__(self):
		# append a 1 to the end of the current row
		self.row.append(1)
		self.row_number += 1

		# starting from the second last element (once there are at least 3)
		# increment it by the element in front of it
		#
		# note: it MUST be iterated from end-to-start as we are modifying the array
		#       and it needs to be adding the values from the previous row
		for i in range(self.row_number, 0, -1):
			self.row[i] += self.row[i - 1]

		# finally, return the new row
		return self.row

n = get_next_type('How many rows of Pascal\'s triangle should be printed? ', int, lambda x: x > 0)

# create a new Pascal instance
pascal = Pascal()

# call the iterator on the Pascal instance
#
# note: the variable `rows` is not needed as `pascal` is mutated
#       and __iter__ returns itself. however, it's good to show that
#       a new iterator instance would be used if it existed
rows = iter(pascal)

# print out `n` rows
# we can use a spread operator to separate each element
# in the list by a space (default), or if the question required
# a different delimiter it could be modified with the `sep` kwarg
#
# note: we don't need to handle `next` throwing
#       an error because it never ends
for _ in range(n):
	print(*next(rows))
