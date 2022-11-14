from collections import Counter

f = input('Provide the first string: ')
s = input('Provide the second string: ')

chars = set(f) | set(s)

f_count = Counter(f)
s_count = Counter(s)

for c in chars:
	if f_count.get(c) != s_count.get(c):
		print('These strings are not anagram.')

		break
else:
	print('These strings are anagram.')
