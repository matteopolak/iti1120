def is_repeated(s: str, l: int) -> bool:
	'''
	This function assumes `s` is divisible into equal
	slices of length `l`
	'''

	# get the number of repetitions that are needed to create a
	# string of equal length
	rep = len(s) // l

	# get a string slice and multiply it, then check if it's equal
	#
	# note: we can always slice from the start because the repeated string must
	# cover the entire string, which would only be possible if it started from
	# the beginning of the string
	if s[0:l] * rep == s:
		# if it is, that is a repeating sequence in the string
		return True

	return False


def is_boring(s: str) -> bool:
	# cache the length of the string
	length = len(s)

	# from [1, length // 2), only check numbers that `length` is divisible by
	# note: we can skip everything that is over half of the string as it cannot
	# form more than one repeated string
	for l in filter(lambda x: length % x == 0, range(1, length // 2 + 1)):
		if is_repeated(s, l):
			return True

	# if nothing is found, there are no repeats
	return False


strings = input('Provide alphanumeric strings separated by a space: ').split(
    ' ')

for s in strings:
	if is_boring(s.lower()):
		print(s, end=' ')