import sys
import networkx as nx
from copy import deepcopy
from random import random

sys.setrecursionlimit(10000)


def create_board():
    """Reads the Minesweeper board configuration from board.txt"""
    with open('board.txt', 'r') as f:
        arr = f.readlines()
    arr = [list(line.strip()) for line in arr]
    return arr


def find_neighbors(x, y):
    """To find the neighbors of a cell positioned at (x, y) in the board"""
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if (i, j) != (x, y) and 0 <= i < len(
                    board) and 0 <= j < len(board[0]):
                yield (i, j)


def distance(x1, y1, x2, y2):
	"""Returns the distance between cells (x1, y1) and (x2, y2)"""
	return max(abs(x1 - x2), abs(y1 - y2))


def create_disjoint_sets(unexplored_neighbors):
	"""Creates disjoint sets of cells from the list of unexplored neighbors"""
	st = set(unexplored_neighbors)
	G = nx.Graph()
	disjoint_ls = []
	for x, y in discovered_cells:
		neighbors = list(find_neighbors(x, y))
		neighbors = list(st & set(neighbors))
		for index1, neighbor1 in enumerate(neighbors):
			for index2, neighbor2 in enumerate(neighbors, start=index1 + 1):
				a, b = unexplored_neighbors.index(
				    neighbor1), unexplored_neighbors.index(neighbor2)
				G.add_edge(a, b)
	for i in range(len(unexplored_neighbors)):
		G.add_node(i)
	for ls in nx.algorithms.components.connected_component_subgraphs(G):
		ls = list(ls)
		arr = [unexplored_neighbors[i] for i in ls]
		disjoint_ls.append(arr)
	return disjoint_ls


def find_unexplored_neighbors(unexplored_neighbors):
    """To maintain a list of all immediate neighbors of the already explored cells of the board. These are the cells to which we can assign either mine, safe or uncertain marks."""
    while unexplored_neighbors:
        unexplored_neighbors.pop()
    st = set()
    for x, y in discovered_cells:
        for neighbor_x, neighbor_y in find_neighbors(x, y):
            if (neighbor_x, neighbor_y) not in discovered_cells and (
                    neighbor_x, neighbor_y) not in st:
                unexplored_neighbors.append((neighbor_x, neighbor_y))
                st.add((neighbor_x, neighbor_y))


def solve(ls):
    """This function generates all the possible configurations of mines and clear cells and updates the counts in board_counts dictionary. The probabilities are later calculated based on these counts."""
    mapping = dict()
    for index, value in enumerate(ls):
    	mapping[value] = index
    bit_count = len(ls)
    n = 2 ** bit_count
    for k in range(n):
        if is_valid_config(k, n, bit_count, mapping, ls):
        	update_counts(ls, k, bit_count, board_counts, mapping)


def update_counts(ls, k, bit_count, board_counts, mapping):
    """Updating the counts for a given valid configuration."""
    for x, y in ls:
        if is_set_bit(x, y, k, bit_count, mapping):
            if (x, y) in board_counts:
                board_counts[(x, y)] = (board_counts[(x, y)]
                                        [0] + 1, board_counts[(x, y)][1])
            else:
                board_counts[(x, y)] = (1, 0)
        else:
            if (x, y) in board_counts:
                board_counts[(x, y)] = (board_counts[(x, y)]
                                        [0], board_counts[(x, y)][1] + 1)
            else:
                board_counts[(x, y)] = (0, 1)


def is_set_bit(x, y, k, bit_count, mapping):
	"""Returns True if the mp_index bit is set in the number k"""
	mp_index = bit_count - mapping[(x, y)] - 1
	return True if k & (1 << mp_index) else False


def is_neighbor(x1, y1, ls):
	"""Returns True is (x1, y1) has a neighbor in list ls"""
	for x, y in ls:
		if distance(x1, y1, x, y) == 1:
			return True
	return False


def is_valid_config(k, n, bit_count, mapping, ls):
    """If a configuration is valid, returns True, else False. The configuration is a k-bit """
    for x, y in discovered_cells:
        elem = board[x][y]
        if elem == '.' or elem == '*':
            continue
        if not is_neighbor(x, y, ls):
        	continue
        elem, tmp = int(elem), 0
        surrounding_mines = 0
        for cell in find_neighbors(x, y):
            if cell in mine_cells:
                surrounding_mines += 1
            elif cell in mapping:
                if is_set_bit(*cell, k, bit_count, mapping):
                    surrounding_mines += 1
            elif cell not in mapping and cell not in discovered_cells:
            	tmp += 1
        if tmp + surrounding_mines < elem or surrounding_mines > elem:
        	return False
    return True


def explore(x, y):
    """This function is to explore the cell at position (x, y). Cascading is also a part of this function."""
    if board[x][y] == '*':
    	display_board()
    	print("Game over!")
    	exit()
    discovered_cells.add((x, y))
    if board[x][y] == '.':
        for neighbor_x, neighbor_y in find_neighbors(x, y):
            if (neighbor_x, neighbor_y) not in discovered_cells:
                discovered_cells.add((neighbor_x, neighbor_y))
                if board[neighbor_x][neighbor_y] == '.':
                    discovered_cells.add((neighbor_x, neighbor_y))
                    explore(neighbor_x, neighbor_y)


def display_board():
    """Displays the currently explored parts of the board. The undiscovered parts of the board are displayed with '#'. The cells which AI has marked to be mines are displayed with '$'."""
    tmp = deepcopy(board)
    for i in range(len(board)):
        for j in range(len(board[0])):
            if (i, j) not in discovered_cells:
                tmp[i][j] = '#'
            if (i, j) in mine_cells:
                tmp[i][j] = '$'
    print("Printing the board: ")
    for row in tmp:
        print(''.join(row))
    print('\n')


def calculate_probabilities(board_counts):
	"""Calculates probabilities given the board counts"""
	prob_dict = {}
	for cell, prob in board_counts.items():
		mines, safe = prob
		if mines and not safe:
			mine_cells.add(cell)
		elif not mines and safe:
			safe_cells.add(cell)
		prob_dict[cell] = mines / (mines + safe)
	t = sum(v for v in prob_dict.values() if v != 1)
	remaining_cell_count = cell_count - \
	    len(unexplored_neighbors) - len(mine_cells)
	for i in range(n):
		for j in range(m):
			if (i, j) not in unexplored_neighbors and (i, j) not in discovered_cells:
				prob_dict[(i, j)] = (mines_count - len(mine_cells) - t) / \
				           remaining_cell_count
	return prob_dict


if __name__ == '__main__':
	print("AI trying to solve minesweeper.\n")
	print("The undiscovered parts of the board are represented with '#'.\nThe discovered cells are either integer numbers, '.' or '$' signs.\n'.' represents an already explored clear cell.\n'$' represents a cell which AI has flagged to be a mine.\n")
	unexplored_neighbors = list()
	discovered_cells = set()
	mine_cells, safe_cells = set(), set()
	board = create_board()
	n, m = len(board), len(board[0])
	cell_count = n * m
	mines_count = sum(cell == '*' for row in board for cell in row)
	density = mines_count / cell_count
	if density <= 0.1 or cell_count >= 500:
		limit1, limit2 = 14, 8
	else:
		limit1, limit2 = 16, 12
	print("Board size: {}x{}".format(n, m))
	print("Number of mines:", mines_count)
	disjoint_ls = []
	x, y = 0, 0
	while len(discovered_cells | mine_cells) != cell_count:
		discovered_cells |= mine_cells
		board_counts = {}
		print("Explored ({}, {})".format(x, y))
		explore(x, y)
		display_board()
		find_unexplored_neighbors(unexplored_neighbors)
		disjoint_ls = create_disjoint_sets(unexplored_neighbors)
		for ls in disjoint_ls:
			if len(ls) <= limit1:
				solve(ls)
			else:
				tmp_dict = deepcopy(board_counts)
				for cell in ls:
					ls_new = sorted(ls, key=lambda k:distance(*cell, *k))[:limit2]
					solve(ls_new)
					for t in ls_new:
						if t != cell and t in tmp_dict:
							board_counts[t] = tmp_dict[t]
							a, b = board_counts[cell]
							if a and not b:
								mine_cells.add(cell)
							if b and not a:
								safe_cells.add(cell)
								explore(*cell)
								print("Explored ({}, {})".format(*cell))
								display_board()
		probabilities = calculate_probabilities(board_counts)
		if probabilities:
			x, y = min(probabilities, key=lambda k: (probabilities[k], random()))
			while len(safe_cells) > 1 and len(discovered_cells) + len(mine_cells) < cell_count:
				x, y = safe_cells.pop()
				explore(x, y)
				print("Explored ({}, {})".format(x, y))
				display_board()
		if safe_cells:
			x, y = safe_cells.pop()
	display_board()
	print("Solved it!")	