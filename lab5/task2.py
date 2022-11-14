from math import sqrt

def get_average(data: list[int]):
	return sum(data) / len(data)

def get_sum_square_difference(data: list[int]):
	avg = get_average(data)

	return sum((x - avg) ** 2 for x in data)

def get_stdev(data: list[int]):
	return sqrt(get_sum_square_difference(data) / len(data))

n = int(input('How many data points will you provide? '))
data: list[int] = []

for i in range(1, n + 1):
	data.append(float(input(f'Provide number #{i}: ')))

print(f'The standard deviation is {get_stdev(data)}')
