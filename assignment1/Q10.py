from utils import get_next_type

# n is the number of rows
n = get_next_type('Provide a positive integer for the number of rows: ', int, lambda x: x > 0)

# m is the number of columns
m = get_next_type('Provide a positive integer for the number of columns: ', int, lambda x: x > 0)

# make sure m is never larger than n
if m > n:
	m, n = n, m

# first, we need to get the number of squares in the n by m grid.
# to figure out the equation, let's count the squares of a 4 by 5 grid
#
# 1x1 = 4 * 5
# 2x2 = 3 * 4
# 3x3 = 2 * 3
# 4x4 = 1 * 2
# sum   40
#
# as you can see (and this generalizes), the multiplicand and multiplier
# decrease by 1 as the sides increase by 1
#
# with the power of combinatorics, we can achieve this quite easily
#
#  m
#  E  k(k + d) | where d = n - m
# k=1
#
# now, separate the summation into two (since there's a constant)
#
#  m            m
#  E  k*k  + d  E  k  
# k=1          k=1
#
# now, you may notice that the first term is a sum of squares,
# and the third term is a sum series. let's simplify it using
# their respective formulas, which are already well-known.
#
# m(m + 1)(2m + 1) / 6
# m(m + 1) / 2
#
# now, substitute it all into one big equation:
#
# sq(n, m) = m(m + 1)(2m + 1) / 6 + m(n - m)(m + 1) / 2
#
# finally... write it in Python
squares = m * (m + 1) * (2 * m + 1) // 6 + m * (n - m) * (m + 1) // 2

# let's do the same thing, but with rectangles
#
# note: rectangles include squares, as they are just rectangles
#       whose adjacent sides are congruent
#
# in this case, the number of rectangles is the number of ways
# we can select two horizontal lines and two vertical lines
#
# let a = m + 1, 
#     b = n + 1
#
# re(n, m) = a_C_2 * b_C_2
#          = [a! / (a - 2)!2!] * [b! / (b - 2)!2!]
#          = [(m + 1)! / (m - 1)!2!] * [(n + 1)! / (n - 1)2!]
#          = [m(m + 1) / 2] * [n(n + 1) / 2]
#          = mn(m + 1)(n + 1) / 4
#
# and there we go. now just write it out...
rectangles = m * n * (m + 1) * (n + 1) // 4

print(f'Total number of rectangles = {rectangles}')
print(f'Rectangles but not squares = {rectangles - squares}')
