# Matthew Polak 300286703

from dataclasses import dataclass
from math import sqrt
from typing import Iterator, Literal, Union

Method = Union[Literal['__add__'], Literal['__sub__'], Literal['__mul__']]


@dataclass(slots=True)
class Vector:
	__values: list[float]

	def __init__(self, n=2):
		self.__values = [0.] * n

	@staticmethod
	def from_iter(iterator: Iterator[float]) -> 'Vector':
		vec = Vector(0)
		vec.__values.extend(iterator)

		return vec

	def __get_dimension_or(self, index: int, default: float = 0.) -> float:
		try:
			return self.get_dimension(index)
		except IndexError:
			return default

	def __multiply(self, d: 'float') -> None:
		for i, v in enumerate(self.__values):
			self.__values[i] = v * d

	def __apply_pairwise(self, other: 'Vector', method: 'Method') -> 'Vector':
		dim = max(self.dimension(), other.dimension())
		vec = Vector(dim)

		for i in range(dim):
			vec.set_dimension(
				i,
				getattr(self.__get_dimension_or(i),
				method)(other.__get_dimension_or(i))
			)

		return vec

	def __clone(self):
		return Vector.from_iter(iter(self))

	def dimension(self):
		return len(self.__values)

	def get_dimension(self, index: int):
		return self.__values[index]

	def set_dimension(self, index: int, value: float):
		self.__values[index] = value

	def add_dimension(self, value: float) -> None:
		self.__values.append(value)

	def remove_dimension(self) -> None:
		self.__values.pop()

	def insert_dimension(self, index: int, value: float) -> None:
		self.__values.insert(index, value)

	def erase_dimension(self, index: int) -> None:
		self.__values.pop(index)

	def magnitude(self) -> float:
		return sqrt(sum(map(lambda x: x**2, self.__values)))

	def multiply(self, d: 'float', /) -> 'Vector':
		vec = self.__clone()
		vec.__multiply(d)

		return vec

	def __iter__(self):
		return iter(self.__values)

	def __eq__(self, other: 'Vector') -> bool:
		try:
			return all(
				map(lambda x: x[0] == x[1], zip(self, other, strict=True))
			)
		except ValueError:
			return False

	def __ne__(self, other: 'Vector') -> bool:
		return not self == other

	def __add__(self, other: 'Vector') -> 'Vector':
		return self.__apply_pairwise(other, '__add__')

	def __sub__(self, other: 'Vector') -> 'Vector':
		return self.__apply_pairwise(other, '__sub__')

	def __mul__(self, other: 'Vector') -> 'Vector':
		return self.__apply_pairwise(other, '__mul__')

	def print(self) -> None:
		print(self.__values)
