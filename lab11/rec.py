def sum_integers(n: int) -> int:
	# if n is 1, return 1
	# if n is less than 1, return 0
	#
	# shorthand: max(n, 0)
	if n <= 1:
		return max(0, n)
	# otherwise, return the sum of n and the sum
	# of all integers less than n
	else:
		return n + sum_integers(n - 1)


def sequence(n: int) -> list[int]:
	if n == 1:
		return [1]
	else:
		if n % 2 == 0:
			return [n] + sequence(n // 2)
		else:
			return [n] + sequence(3 * n + 1)


def check(word: str) -> bool:
	# if the word is empty, it is a palindrome
	if len(word) <= 1:
		return True
	else:
		# if the first and last characters are not equal,
		# the word is not a palindrome
		if word[0] != word[-1]:
			return False
		else:
			# otherwise, check the rest of the word by slicing
			# off the first and last characters
			return check(word[1:-1])
