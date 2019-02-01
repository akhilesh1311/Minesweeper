from random import random


def find_neighbors(x, y):
    """To find the neighbors of a cell positioned at (x, y) in the board"""
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i, j) != (x, y) and 0 <= i < len(
                    arr) and 0 <= j < len(arr[0]):
                yield (i, j)


n, m, mines = 16, 16, 30
prob = mines / (n * m)

arr = []

for i in range(n):
	tmp = []
	for j in range(m):
		r = random()
		cell = '*' if r <= prob else '.'
		tmp.append(cell)
	arr.append(tmp)

arr[0][0] = '.'


for i in range(n):
	for j in range(m):
		s = sum(arr[x][y] == '*' for x, y in find_neighbors(i, j))
		if s and arr[i][j] == '.':
			arr[i][j] = str(s)

with open('board_random.txt', 'w') as f:
	for row in arr:
		f.write(''.join(row) + '\n')