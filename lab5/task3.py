def find_index(substring: str, string: str):
	try:
		return (True, string.rindex(substring))
	except ValueError:
		return (False, len(string))

substring = input('Provide the substring: ')
string = input('Provide the parent string: ')

found, index = find_index(substring, string)

print(
	f'{substring} is a substring of {string}\nThe last occurrence of abc is at index {index}.'
	if found else
	f'{substring} is not a substring of {string}\nThe length of the second string is {index}.'
)
ddddddddddd