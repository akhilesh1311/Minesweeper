

class Minesweeper(object):

	""" main class for controlling game logic """

	def __init__(self):
		pass

	def create_game_board(self):
		pass


class Cell(object):

	""" class for handling state of a cell on the game board """

	NEIGHBORS = [
		(-1, -1), (-1, 0), (-1, 1)
		(0, -1), (0, 1),
		(1, -1), (1, 0), (1, 1)
	]

	def __init__(self):
		self.row = None
		self.col = None
		self.is_unknown = True
		self.is_clear = False
		self.is_mine = False
		self.is_clue = False
		

class Board(object):

	""" class for handling state of the game board """

	def __init__(self, nrows, ncols):
		self.nrows = nrows
		self.ncols = ncols
		self.unknown_cells = []
		self.clear_cells = []
		self.mine_cells = []
		self.clue_cells = []