n = int(input('How many integers will you provide (> 2)? '))

one = set()
two = set()

for _ in range(n):
	x = int(input('Provide an integer: '))

	if x in two:
		continue
	elif x in one:
		one.remove(x)
		two.add(x)
	else:
		one.add(x)

print(f'The unique number = {", ".join(map(str, one))}')
