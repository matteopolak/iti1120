# create messages for each prompt
prompts = (
	'What is the slope of the line? ',
	'What is the y-intercept of the line? ',
	'What is the x coordinate (x, ?) of the point? ',
	'What is the y coordinate (?, y) of the point? ',
)

# index must be [0, 3]
def get_next_float(index: int) -> float:
	# get the user's input
	float_str = input(prompts[index])

	# use a try-except block to handle incorrect input
	try:
		# parse the input into an int using the built-in float() function
		# if the string cannot be parsed, it will throw a ValueError exception
		number = float(float_str)

		return number
	# catch the ValueError exception specifically (if the user presses Ctrl+C
	# it WILL allow them to exit, unlike using a raw `except` block)
	except ValueError:
		print(f'Invalid input "{float_str}": must a real number')

		# since the value was incorrect, return the same function to re-try the input
		return get_next_float(index)

# collect all of the inputs
[slope, y_int, point_x, point_y] = [get_next_float(i) for i in range(4)]

# calculate the y-coordinate of the line at x=point_x
equation_point_y = slope * point_x + y_int

# get the sign of the slope (-1 if < 0, otherwise 1)
# this can also be done without an `if` check using `slope / abs(slope)`
slope_sign = 1 if slope >= 0 else -1

# if the y-coordinates are equal, it's not on either side of the line
if equation_point_y == point_y:
	print(f'On the line')

	exit()

# if the slope is positive and the input point_y is less than the y-coordinate
# of the point of the line at that postion
is_left = equation_point_y < point_y

# if the slope is negative, reverse the decision
if slope < 0:
	is_left = not is_left

# get the side of the line (if the slope is 0, left is above and right is under)
side = 'left' if is_left else 'right'

# print out the result
print(f'The {side} side of the line')
