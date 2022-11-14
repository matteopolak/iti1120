from dataclasses import dataclass, field
from math import sqrt, floor


# check if the given number is prime
def is_prime(n: int) -> bool:
	for i in range(2, floor(sqrt(n)) + 1):
		if n % i == 0:
			return False
	return True


@dataclass(slots=True)
class PrimeSum:
	of: int
	end: int = 0
	curr: int = 2
	need: set[int] = field(default_factory=set)

	# restart the iterator
	def __iter__(self):
		self.curr = 2
		self.end = floor(sqrt(self.of)) + 1

		return self

	# get the next combination of primes that sum to `self.of`
	# (overkill because we only need one)
	def __next__(self):
		for i in filter(is_prime, range(self.curr, self.of)):
			r = self.of - i

			if r in self.need:
				return r, i
			else:
				self.need.add(i)

		return (None, None)


n = int(
    input('Provide the integer you want to find a sum of two primes for: '))

prime = PrimeSum(n)

# get the first combination of primes that sum to `n`
a, b = next(iter(prime))

# print them out in the required format
print(f'{n} = {a} + {b}')
