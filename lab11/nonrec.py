def sumIntegers(n):
	sum = 0

	for i in range(1, n + 1):
		sum += i

	return sum


def sequence(n):
	seq = []

	while n != 1:
		seq.append(n)

		if n % 2 == 0:
			n = n // 2
		else:
			n = 3 * n + 1

	seq.append(1)

	return seq


def check(word):
	n = len(word)
	i = 0
	j = n - 1

	while i < j:
		if word[i] != word[j]:
			return False

		i = i + 1
		j = j - 1

	return True