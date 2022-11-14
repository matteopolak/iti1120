from math import sqrt

# create messages for each prompt
prompts = (
	'What is `a` in the equation "ax^2 + bx +c"?: ',
	'What is `b` in the equation "ax^2 + bx +c"?: ',
	'What is `c` in the equation "ax^2 + bx +c"?: ',
)

# index must be [0, 2]
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

# get the coefficients of the equation
[a, b, c] = [get_next_float(i) for i in range(3)]

# check if it is a linear equation
if a == 0:
	# derive the single root from y=bx+c into x=-c/b
	print(f'Root = {-c / b}')

	exit()

# calculate "b^2 - 4ac" from the quadratic equation
under_root = b ** 2 - 4 * a * c

# if the number inside of the square root is less than 0,
# there are no real solutions
if under_root < 0:
	print('No Root')

	exit()

# calculate "-b / 2a", the first portion of the equation
divided_b = -b / (2 * a)

# if the number under the root is zero, there is only one root
# and it's equal to "-b / 2a"
if under_root == 0:
	print(f'Root = {divided_b}')

	exit()

# take the square root of the number inside of the root
# and divide it by "2a" (the second portion of the equation)
#
# note: `under_root` could be raised to the power of 0.5 instead
# of using the `sqrt` function from the math library
divided_root = sqrt(under_root) / (2 * a)

# calculate both roots (there must be two distinct and real roots now)
# and print them out
print(f'Root 1 = {divided_b + divided_root}')
print(f'Root 2 = {divided_b - divided_root}')
