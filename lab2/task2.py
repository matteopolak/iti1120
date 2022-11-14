a = int(input('Provide a value for `a`: '))
q = int(input('Provide a value for `q`: '))
n = int(input('Provide a value for `n`: '))

# print out the first number
print(f'{a}', end='')

# multiply `a` by `q` and print it n - 1 times
for _ in range(n - 1):
	a *= q

	print(f', {a}', end='')
