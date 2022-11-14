first = input().split(' ')
second = input().split(' ')


def get_common_ends(one: list[str], two: list[str]) -> int:
	# cache last value
	last = one[-1]

	# initialize the end variable
	end = None

	try:
		# find the index in the second list where the value is equal to the
		# last element in the first list
		end = second.index(last) + 1
	except ValueError:
		# if there is none, they're unique so there's no overlap
		return 0

	# set the index to start at
	start = len(first) - end

	# iterate through both lists, starting at `start` for the first one,
	# and ending at `end` (-1) for the second
	#
	# for example:
	# 1 0 2 9 7 6 4
	# 7 6 4 2 3 5 7
	#
	# with end=3 and start=4
	# (7, 7), (6, 6), (4, 4)
	for a, b in zip(first[start:], second[0:end]):
		# if they're not equal at any point, there's no overlap
		if a != b:
			return 0

	# finally, return the number of overlapped elements on each end
	return end


# slice off the repeated elements from the second list, then concat and print
print(first + second[get_common_ends(first, second):])