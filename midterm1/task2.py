from collections import defaultdict


def combine(midterm: dict[str, int], final: dict[str, int]) -> dict[str, int]:
	# create a dictionary that defaults the value to 0 if the key
	# does not exist upon insert
	grades = defaultdict[str, int](lambda: 0)

	# add grades to the student for midterm and final
	for student, grade in final.items():
		grades[student] += grade

	for student, grade in midterm.items():
		if student not in final:
			grades[student] = 0
		else:
			grades[student] += grade

	# then return the dictionary (can't return a defaultdict because
	# the output is a dict, not a defaultdict)
	return dict(grades)
