from math import inf
from functools import reduce
from typing import Tuple

def return_smallest(prev: Tuple[float, float], curr: Tuple[float, float]):
	# the second element is always larger than the first
	# because we sorted it
	if (prev[1] - prev[0]) <= (curr[1] - curr[0]):
		return prev
	else:
		return curr

n = int(input('Provide a positive integer >= 2: '))

# store all inputs here
numbers = [
	float(input('Provide a real number: '))
	for _ in range(n)
]

# sort in ascending order
# time complexity of O(nlogn)
numbers.sort()

# time complexity of O(n)
one, two = reduce(
	return_smallest,
	zip(numbers, numbers[1:]),
	(-inf, inf)
)

# overall time complexity of O(n + nlogn) = O(nlogn)
# since n < nlogn as they go to infinity
print(one, two)
