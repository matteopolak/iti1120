from dataclasses import dataclass
from math import floor

LF = '\n'
LETTERS = ('F', 'E', 'D', 'D+', 'C', 'C+', 'B', 'B+', 'A-', 'A', 'A+')
MARKS = (
	('Lab mark', 10, 0.1),
	('Assignment 1', 30, 0.05),
	('Assignment 2', 30, 0.05),
	('Assignment 3', 30, 0.05),
	('Assignment 4', 30, 0.05),
	('Assignment 5', 30, 0.05),
	('Term test', 15, 0.15),
	('Midterm', 20, 0.2),
	('Final exam', 30, 0.3)
)

@dataclass(slots=True)
class Mark:
	name: str
	grade: float
	weight: float

	@property
	def weighted(self):
		return self.weight * self.grade

	def __str__(self):
		return f'{self.name}: {self.weighted * 100:g}%'

	def build(self, weight_sum: float):
		self.weight /= weight_sum

@dataclass(slots=True)
class Student:
	name: str
	f_name: str
	l_name: str
	marks: list[Mark]
	weight_sum: float
	__average: float | None

	def __init__(self, name: str):
		self.name = name
		self.f_name, self.l_name = name.split(' ')
		self.marks = []
		self.weight_sum = 0
		self.__average = None

	def add_mark(self, mark: 'Mark'):
		self.weight_sum += mark.weight
		self.marks.append(mark)

	def build(self):
		for mark in self.marks:
			mark.build(self.weight_sum)

	@property
	def average(self):
		if self.__average:
			return self.__average

		self.__average = sum(mark.weighted for mark in self.marks)

		return self.__average

	@property
	def letter(self):
		return LETTERS[floor((self.average * 100 - 40) / 5)]

def process_student() -> 'Student':
	student = Student(input('What is the student\'s full name? '))

	for name, out_of, weight in MARKS:
		grade = float(input(f'How many marks did {student.name} get for {name}? '))
		student.add_mark(Mark(name, grade / out_of, weight))

	student.build()

	return student

n = int(input('How many students are you processing? '))
students = [process_student() for _ in range(n)]

for i, student in enumerate(students):
	print(f'''Student {i + 1}:
Firstname: {student.f_name}
Lastname: {student.l_name}
{LF.join(map(str, student.marks))}
Final mark: {student.average}
Letter grade: {student.letter}''')
