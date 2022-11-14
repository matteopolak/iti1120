from utils import get_next_type

# to calculate the mode, a dictionary is created
# with a tally of each number in the dataset
#
# the number(s) with the highest count(s) are returned
def calculate_mode(data: list[int]):
	# create the dictionary
	mode_dict: dict[int, int] = {}

	# create a variable to track the highest count
	mode_count = 0

	# create a list to store the numbers with the highest
	# counts so the dictionary doesn't need to be sorted
	#
	# the caveat to this is that clearing and appending to
	# an array in Python is pretty slow, so this is probably
	# slower than just sorting the dictionary if the dataset
	# is very large
	mode: list[int] = []

	for n in data:
		# if the number is already in the dictionary, increment the count
		if n in mode_dict:
			mode_dict[n] += 1
		# otherwise, initialize it at a count of 1
		else:
			mode_dict[n] = 1

		# if the count of the current number is greater
		# than the highest, update the mode
		if mode_dict[n] > mode_count:
			mode.clear()
			mode_count = mode_dict[n]
			mode.append(n)
		# if it's equal, append it to the current numbers
		elif mode_dict[n] == mode_count:
			mode.append(n)
		# otherwise... do nothing

	return mode

n = get_next_type('How many numbers are in the dataset? ', int, lambda x: x > 0)

# collect all of the data into an array
# using list comprehension
data = [get_next_type(f'Dataset entry {i}: ', float) for i in range(1, n + 1)]

# sort the data in ascending order (i.e. lowest to highest)
#
# note: this must be done in order to calculate the median
data.sort()

# calculate the average by diving the sum of the data
# by the number of data points
average = sum(data) / n

# get the median
median = data[(n - 1) // 2] if n % 2 else (data[n // 2] + data[n // 2 - 1]) / 2

# `span` is the range but it's better to avoid naming variables
# the same name as a built-in function (i.e. range)
span = max(data) - min(data)

# calculate the mode
mode = calculate_mode(data)

# print the results to stdout
print(f'Average = {average}')
print(f'Modes = {", ".join(map(str, mode))}')
print(f'Median = {median}')
print(f'Range = {span}')
