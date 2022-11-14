# the number of digits to read from stdin
# note: the `pretty` tuple must have at least NUM_DIGITS entries
NUM_DIGITS = 3

# create a tuple for pretty prompt messages:
# ... the (first|second|third) digit ...
pretty: tuple[str, str, str] = ('first', 'second', 'third')

# index must be [0, NUM_DIGITS - 1]
def get_next_digit(index: int) -> int:
	# get the user's input
	digit_str = input(f'Provide the {pretty[index]} digit from 0 to 9: ')

	# use a try-except block to handle incorrect input
	try:
		# parse the digit into an int using the built-in int() function
		# if the string cannot be parsed, it will throw a ValueError exception
		digit = int(digit_str)

		# if the number is negative or greater than 9 (i.e. not a single digit)
		# raise the ValueError so all incorrect entries are handled in the same place
		if digit < 0 or digit > 9:
			raise ValueError

		return digit
	# catch the ValueError exception specifically (if the user presses Ctrl+C
	# it WILL allow them to exit, unlike using a raw `except` block)
	except ValueError:
		print(f'Invalid input "{digit_str}": must a number between 0 and 9')

		# since the value was incorrect, return the same function to re-try the input
		return get_next_digit(index)

# collect three digits
digits = [get_next_digit(i) for i in range(NUM_DIGITS)]

# sort the digits in ascending order using the `sorted` built-in
# then map the digits to strings using the `map` built-in
# then join them into a string by using str#join
smallest_digit_str = ''.join(map(str, sorted(digits)))

# reverse the string to get the smallest number
# note: the same steps as above could be used by passing the
# sorted=True keyword argument to the `sorted` function, but reversing
# the string is over 6 times faster (0.76s v.s. 4.87s for 10 million runs)
largest_digit_str = smallest_digit_str[::-1]

# print out the results
# note: the built-in int() function will strip leading zeros
print(f'Largest = {int(largest_digit_str)}')
print(f'Smallest = {int(smallest_digit_str)}')
