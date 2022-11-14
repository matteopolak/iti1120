from utils import get_next_type
from dataclasses import dataclass, field
from typing import Union

# this is used as a pseudo-map to convert
# indexes to x, y, and z
#
# 0 -> x
# 1 -> y
# 2 -> z
n_to_c = (
	'x',
	'y',
	'z'
)

# this class is a vector in 3-space or a 3,1 matrix
@dataclass(slots=True)
class Vec3:
	x: int
	y: int
	z: int

	# clones the vector
	def clone(self):
		return Vec3(self.x, self.y, self.z)

	# returns `True` if the two vectors are co-linear
	def eq_dir(self, other: 'Vec3', /):
		mul = self.get_multiple(other)

		if mul is None:
			return False

		return self.x * mul == other.x and self.y * mul == other.y and self.z * mul == other.z

	# returns a scalar that, when multiplied by the current vector,
	# results in the second vector
	def get_multiple(self, other: 'Vec3', /) -> Union[float, None]:
		s = 'x' if self.x and other.x else 'y' if self.y and other.y else 'z' if self.z and other.z else None

		if s is None:
			return None

		return other[s] / self[s]

	# returns the cross product of two vectors
	def cross(self, other: 'Vec3', /) -> 'Vec3':
		return Vec3(
			self.y * other.z - self.z * other.y,
			self.z * other.x - self.x * other.z,
			self.x * other.y - self.y * other.x
		)

	# required when using subscript notation to get coordinates
	# e.g. `vec[idx]` where idx = 'x' | 'y' | 'z'
	def __getitem__(self, item):
		return getattr(self, item)

	# returns `True` if the vector is a zero vector
	def is_zero(self):
		return self.x == 0 and self.y == 0 and self.z == 0

	# returns the dot product of two vectors
	def dot(self, other: 'Vec3', /):
		return self.x * other.x + self.y * other.y + self.z * other.z

	# returns the scalar multiplication of a vector
	def mul(self, scalar: float, /):
		return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)

# this is a 3,3 matrix, or three rows of vectors in 3-space
@dataclass(slots=True, repr=True)
class Matrix33:
	rows: list['Vec3'] = field(default_factory=list)
	cols: list['Vec3'] = field(default_factory=list)

	# when initializing the 3,3 matrix,
	# an array with 3 Vec3s is required to build it
	def __init__(self, rows: list['Vec3']):
		self.rows = rows
		self.cols = []

		# create another array for the columns,
		# which can be used to easily transpose the matrix
		for i in range(len(rows)):
			self.cols.append(Vec3(*map(lambda x: x[n_to_c[i]], rows)))

	# returns `True` if all rows are 0
	def is_zero(self) -> bool:
		return all(map(lambda v: v.is_zero(), self.rows))

	# returns the dot of two matrices
	def dot(self, other: 'Matrix33', /):
		rows = [0, 0, 0, 0, 0, 0, 0, 0, 0]

		for i, v in enumerate(self.rows):
			for j, w in enumerate(other.cols):
				rows[i * 3 + j] = v.dot(w)

		return Matrix33([
			Vec3(rows[0], rows[1], rows[2]),
			Vec3(rows[3], rows[4], rows[5]),
			Vec3(rows[6], rows[7], rows[8]),
		])

	# returns the determinant of the matrix
	def det(self):
		return (
			self.rows[0].x * (self.rows[1].y * self.rows[2].z - self.rows[1].z * self.rows[2].y) +
			self.rows[0].y * (self.rows[1].z * self.rows[2].x - self.rows[1].x * self.rows[2].z) +
			self.rows[0].z * (self.rows[1].x * self.rows[2].y - self.rows[1].y * self.rows[2].x)
		)

	# returns the transposition of the matrix
	def tsp(self):
		return Matrix33(self.cols)

	# returns the cofactor of the matrix
	def cof(self):
		return Matrix33([
			Vec3(
				self.rows[1].y * self.rows[2].z - self.rows[1].z * self.rows[2].y,
				self.rows[1].z * self.rows[2].x - self.rows[1].x * self.rows[2].z,
				self.rows[1].x * self.rows[2].y - self.rows[1].y * self.rows[2].x,
			),
			Vec3(
				self.rows[0].z * self.rows[2].y - self.rows[0].y * self.rows[2].z,
				self.rows[0].x * self.rows[2].z - self.rows[0].z * self.rows[2].x,
				self.rows[0].y * self.rows[2].x - self.rows[0].x * self.rows[2].y,
			),
			Vec3(
				self.rows[0].y * self.rows[1].z - self.rows[0].z * self.rows[1].y,
				self.rows[0].z * self.rows[1].x - self.rows[0].x * self.rows[1].z,
				self.rows[0].x * self.rows[1].y - self.rows[0].y * self.rows[1].x,
			),
		])

	# returns the adjoint matrix
	def adj(self):
		return self.cof().tsp()

	# multiplies the matrix by a scalar
	def mul(self, scalar, /):
		return Matrix33(list(map(lambda x: x.mul(scalar), self.rows)))

prompts = (
	'Provide `a` for "ax + by + c = d"',
	'Provide `b` for "ax + by + c = d"',
	'Provide `c` for "ax + by + c = d"',
	'Provide `d` for "ax + by + c = d"',
)

def get_next_plane(index: int):
	# `ax + by + cz = d` values
	a, b, c, d = [get_next_type(f'{prompts[i]} for plane {index + 1}: ', float) for i in range(4)]

	# returns a normal vector and a vector with just the `d` variable in the first position.
	# the second vector is used to construct a 3,1 matrix but when doing operations it's much easier
	# to just re-use the 3,3 matrix functionality since it will result in the same answer in this case
	return (
		Vec3(a, b, c),
		Vec3(d, 0, 0)
	)


# `False` if the planes are parallel and not coincident, `True` otherwise.
#
# we use a trailing slash to force `first` and `second` to be positional-only,
# since their names don't really hold any meaning
def can_intersect(first: tuple['Vec3', 'Vec3'], second: tuple['Vec3', 'Vec3'], /):
	# check if the normal vectors are parallel
	if first[0].eq_dir(second[0]):

		# `c` cannot be None here, since they share direction
		c = first[0].get_multiple(second[0])

		# return `True` if the equations are scalar multiples
		# we already know the normals are co-linear
		#
		# so this is checking if `d` in `ax + by + cz = d` is equal
		# in order to show the two equations are the same
		return first[1].x * c == second[1].x

	return True

# get three planes
planes = [get_next_plane(i) for i in range(3)]

# if any of the planes cannot intersect with the other,
# there is no intersection at all
#
# note: there are other ways to determine if the planes
# do not intersect, but this is good enough for the problem
if not can_intersect(planes[0], planes[1]) or not can_intersect(planes[0], planes[2]) or not can_intersect(planes[1], planes[2]):
	print('No answer found!')

	exit()

# creates a 3,3 matrix of the normal vectors of the planes
normals = Matrix33(list(map(lambda p: p[0], planes)))

# creates a 3,1 matrix (columns 2 and 3 are zeroed)
constants = Matrix33(list(map(lambda p: p[1], planes)))

# get the determinant of the normals (checks if they are co-linear)
determinant = normals.det()

# if the determinant of the normals matrix is 0,
# the planes are either intersect on a line or are all coincident
#
# note: they cannot be parallel and not coincident as this condition
#       is checked at the start
if determinant == 0:
	print('There are infinite number of answers!')

	# exit to make sure the branch below is not executed
	# this could also be done with if-else but it's better
	# to indent as little as possible
	exit()

# get the adjoint of the normals matrix
adjoint = normals.adj()

# to solve the linear equation, we need to get the inverse of the
# matrix and dot it with the 3,1 constants matrix
#
# however, since we already have the determinant, we can use the fact
# that the inverse is the adjoint matrix divided by the determinant
# and dotted with the constants
#
# this will result in a matrix where the first column
# is the x, y, and z values
inverse = adjoint.mul(1 / determinant)
point = inverse.dot(constants)

print(f'x = {point.cols[0].x:f}')
print(f'y = {point.cols[0].y:f}')
print(f'z = {point.cols[0].z:f}')
