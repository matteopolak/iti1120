from typing import Type, TypeVar, Union, Callable

# `T` is a generic (it's initialized very weirdly in Python)
# with the restraint that it must be a str, float, or int
T = TypeVar('T', str, float, int)

# this is a very generic function that converts input into some type of number
# a generic must be used to give the typehint that the type of `number_type`
# will be equal to the type of the output
#
# `prompt` is a string that is sent in the input prompt
# `number_type` is the type that the input should be converted to
# `f` is either a filter or None
#
# the typehint looks a bit complicated, so i will elaborate on it
# Union[Callable[[T], bool], None]
#
# overall, it is a union of two types:
# Callable[[T], bool]
# None
#
# None is the type given when a function is not provided
# Callable[[T], bool] is a function that has one argument, `T`,
# and output `bool`. this is usually given as a lambda.
#
# as mentioned before, `T` is the type of `number_type` and therefore must be
# the type passed to the lambda as the converted input is filtered
def get_next_type(prompt: str, number_type: Type[T], f: Union[Callable[[T], bool], None] = None, /) -> T:
	# use a try-except block to retry the prompt if the 
	# user provides incorrect input
	try:
		# get the input and convert it
		#
		# note: if the input cannot be converted to int or float,
		#       it will raise a ValueError which is caught below
		number = number_type(input(prompt))

		# if `f` exists and `number` does not pass (i.e. the function
		# returns False), raise a ValueError so it is also caught below
		if f and not f(number):
			raise ValueError

		# otherwise, return the number
		return number
	except ValueError:
		# this block is executed when the input is invalid,
		# so it's a good idea to tell the user their input was bad
		print('Invalid input. Please try again.')

		# then, execute the function again
		return get_next_type(prompt, number_type, f)
