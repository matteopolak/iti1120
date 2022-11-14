from enum import Enum
from re import Pattern, compile

'''
The number of colours in the code.
'''
NUM_COLOURS: int = 4

'''
The regex to split input by.
'''
SPLIT_REGEX: Pattern[str] = compile(r'\s+')

'''
An enum containing every possible colour.
'''
class Colour(Enum):
	RED = 'Red'
	YELLOW = 'Yellow'
	BLUE = 'Blue'
	GREEN = 'Green'
	ORANGE = 'Orange'
	PINK = 'Pink'
	PURPLE = 'Purple'
	CYAN = 'Cyan'
	SILVER = 'Silver'
	TEAL = 'Teal'

def pluralize(n: int, /, plural: str, singular: str, singular_zero: bool = False):
	'''
	@param plural: The string to use if :ref:`n` is != 1
	@param singular: The string to use if :ref:`n` == 1

	@returns :ref:`singular` if :ref:`n` == 1 else :ref:`plural`

	```py
	pluralize(1, "dogs", "dog") # dog
	pluralize(4, "dogs", "dog") # dogs
	```
	'''
	return singular if n == 1 or (singular_zero and n == 0) else plural
