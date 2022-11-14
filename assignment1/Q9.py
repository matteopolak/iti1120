substring = input('Provide the substring to search for: ')
parent = input('Provide the string to search in: ')

# use a set to handle the case where `-0` and `0`
# are both answers (therefore duplicates), which occurs
# when the substring is of length 1 and is present at the
# start of the parent string
indexes: set[int] = set()

# represents the last index checked. this is used when
# searching for the next occurrence of the string
# with str#find
last_index = 0

# the length of the string
#
# treat a blank string as having a length of 1
# so it correctly handles the case where it looks for
# a blank string in a blank string. without the minimum of 1,
# this case would return {0, 1} instead of the correct answer
# of {0}
str_len = max(len(substring), 1)

# we don't know how many occurrences there could be,
# and we don't care about the index so it's best to just
# use a `while` loop
while True:
	# `i` is the next index of the string in the list
	i = parent.find(substring, last_index)

	# if the index is -1, there are no more occurrences
	if i == -1:
		break

	# add the index to the set
	indexes.add(i)

	# finally, update the index to the current checked
	# index plus one so we don't loop forever
	last_index = i + 1

# reverse the string
substring = substring[::-1]

# reset the index tracker
last_index = 0

# do the exact same thing as before, but use a negative index
#
# note: in the example it looks like the length of the string is
#       also removed (technically added and then all of it is negated)
#       so the same will be done here
while True:
	# ...
	i = parent.find(substring, last_index)

	# ...
	if i == -1:
		break

	# make the index negative and relative to
	# the *end* of the substring
	indexes.add(-i - str_len + 1)

	# ...
	last_index = i + 1

# sort the numbers
#
# the key used to sort is a tuple with the following elements:
# 0 -> the absolute value of the number
# 1 -> the value
#
# negative numbers come before positive ones in ascending order,
# so we just need to know the fact that tuples are sorted from
# their first element to their last (that is, subsequent elements
# are only compared if the previous are equal)
#
# since x must either be a or -a, -a will be sorted before a
# in all cases because abs(a) must be equal
#
# finally, format the indexes like {a, b, c, ..., x, y, z}
print(f'{{{", ".join(map(str, sorted(indexes, key=lambda x: (abs(x), x))))}}}')
