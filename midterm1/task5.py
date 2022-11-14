# gets a list from stdin
def get_next_list(i: int) -> list[float]:
	n = int(input(f'Provide the number of elements for list {i}: '))

	return [
	    float(input(f'Provide element {j} for list {i}: '))
	    for j in range(1, n + 1)
	]


# get two lists
a, b = [get_next_list(i) for i in range(1, 3)]

# create a list to store the merged lists
merge: list[float] = []

# iterate through one of them (either works)
for n in a:
	# while b has elements at the first element is smaller than
	# the current element from a, pop it and add it
	while b and b[0] < n:
		merge.append(b.pop(0))

	# now, `n` must be greater than or equal to the first element in b,
	# or b is empty
	merge.append(n)

# if b has elements remaining, add all of them to
# the end of the merge list
if b:
	merge.extend(b)

print(merge)
