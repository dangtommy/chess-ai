import numpy as np

'''

Board class

'''

class Board:

	# Pieces
	# Pieces are defined by value % 10.
	# White/black are differentiated by /10.

	WHITE_KING = 1
	WHITE_QUEEN = 2
	WHITE_BISHOP = 3
	WHITE_KNIGHT = 4
	WHITE_ROOK = 5
	WHITE_PAWN = 6
	WHITE_FIRST_PAWN = 7
	WHITE_FIRST_KING = 8
	WHITE_FIRST_ROOK = 9

	BLACK_KING = 11
	BLACK_QUEEN = 12
	BLACK_BISHOP = 13
	BLACK_KNIGHT = 14
	BLACK_ROOK = 15
	BLACK_PAWN = 16
	BLACK_FIRST_PAWN = 17
	BLACK_FIRST_KING = 18
	BLACK_FIRST_ROOK = 19

	def __init__(self):
		self.board = np.zeros([8, 8])
		# TODO: Move board turn here. Maybe combine with board_start.
		self.board_start = 0
		self.init_board()
		print(str(self.board))
		self.threat_board = [[[] for j in range(0, 8)] for i in range(0, 8)]
		self.threat_board = self.update_threats()

	# Initialize board to beginning state
	def init_board(self):
		# self.board_start
		# 1 - play as black
		# 0 - play as white
		if self.board_start:
			# White pieces
			self.board[0, 3] = self.WHITE_FIRST_KING
			self.board[0, 4] = self.WHITE_QUEEN
			self.board[0, 2] = self.board[0, 5] = self.WHITE_BISHOP
			self.board[0, 1] = self.board[0, 6] = self.WHITE_KNIGHT
			self.board[0, 0] = self.board[0, 7] = self.WHITE_FIRST_ROOK
			self.board[1,:] = self.WHITE_PAWN
			# Black pieces
			self.board[7, 3] = self.BLACK_FIRST_KING
			self.board[7, 4] = self.BLACK_QUEEN
			self.board[7, 2] = self.board[7,5] = self.BLACK_BISHOP
			self.board[7, 1] = self.board[7,6] = self.BLACK_KNIGHT
			self.board[7, 0] = self.board[7,7] = self.BLACK_FIRST_ROOK
			self.board[6,:] = self.BLACK_PAWN
		else:
			# White pieces
			self.board[7, 4] = self.WHITE_FIRST_KING
			self.board[7, 3] = self.WHITE_QUEEN
			self.board[7, 2] = self.board[7,5] = self.WHITE_BISHOP
			self.board[7, 1] = self.board[7,6] = self.WHITE_KNIGHT
			self.board[7, 0] = self.board[7,7] = self.WHITE_FIRST_ROOK
			self.board[6,:] = self.WHITE_PAWN
			# Black pieces
			self.board[0, 4] = self.BLACK_FIRST_KING
			self.board[0, 3] = self.BLACK_QUEEN
			self.board[0, 2] = self.board[0, 5] = self.BLACK_BISHOP
			self.board[0, 1] = self.board[0, 6] = self.BLACK_KNIGHT
			self.board[0, 0] = self.board[0, 7] = self.BLACK_FIRST_ROOK
			self.board[1,:] = self.BLACK_PAWN

		# Reset all other squares to 0.
		self.board[5,:] = self.board[4,:] = \
			self.board[3,:] = self.board[2,:] = 0

	# Updates square at this position
	def update_square(self, x, y, val):
		self.board[x, y] = val;

	# Update threat board.
	def update_threats(self):
		print('updating threats')
		piece_and_threats = []

		# Collect all the valid moves each piece can make
		for i in range (0, 8):
			for j in range(0, 8):
				threats = self.get_valid_moves_at_square(i, j)
				piece_and_threats.append([self.board[i, j], threats])

		# Reset threat board
		self.threat_board = [[[] for j in range(0, 8)] for i in range(0, 8)]

		# For each of
		# Threat board [x, y] += threatening piece
		for x in piece_and_threats:
			if not x[1] == None:
				for square in x[1]:
					self.threat_board[square[0]][square[1]].append(x[0])
		return self.threat_board

	# Make sure the position is valid for movement.
	def validate_position(self, pos):
		if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7:
			return True
		return False

	# Helper function for checking threatened squares.
	def line_helper(self, pos, i_max, j_max, i_inc, j_inc, attack_end):
		valid_moves = []
		x = pos[0] + i_inc
		y = pos[1] + j_inc

		# Continue in this direction while empty squares, legal,
		# and have yet to hit our max desired distance.
		while x != i_max and y != j_max and self.validate_position([x, y]) and \
			self.board[x, y] == 0:
			valid_moves.append([x, y])
			x += i_inc
			y += j_inc

		# Check if we've hit enemy piece at the end.
		if 	attack_end and self.validate_position([x, y]) and \
			not self.board[x, y] == 0 and not (int)(self.board[x, y] / 10) == \
			(int)(self.board[pos[0], pos[1]] / 10):
			valid_moves.append([x, y])

		return valid_moves

	# Return a list of legal moves to this square
	def get_valid_moves_at_square(self, x, y):
		valid_moves = []
		if self.board[x, y] % 10 == 1 or self.board[x, y] % 10 == 8:
			valid_moves = self.get_king_moves([x, y])
		elif self.board[x, y] % 10 == 2:
			valid_moves = self.get_queen_moves([x, y])
		elif self.board[x, y] % 10 == 3:
			valid_moves = self.get_bishop_moves([x, y])
		elif self.board[x, y] % 10 == 4:
			valid_moves = self.get_knight_moves([x, y])
		elif self.board[x, y] % 10 == 5 or self.board[x, y] % 10 == 9:
			valid_moves = self.get_rook_moves([x, y])
		elif self.board[x, y] % 10 == 6 or self.board[x, y] % 10 == 7:
			valid_moves = self.get_pawn_moves([x, y])
		return valid_moves

	# Return the value of the piece at the coordinates.
	def get_piece(self, x, y):
		return self.board[x, y]

	# Return threat board.
	def get_threat_board(self):
		return self.threat_board

	# Check if the piece at pos is currently being attacked.
	def check_square_threatened(self, pos, player):
		for threat in (self.get_threat_board())[pos[0]][pos[1]]:
			if not (int) (threat / 10) == player:
				return True
		return False
	'''
		Movement functionality for each type of piece
	'''
	def get_king_moves(self, pos):
		moves = []
		valid_moves = []

		x = pos[0]
		y = pos[1]

		# Only add legal squares that aren't threatened and aren't friendly.
		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				moves.append([i, j])
		for move in moves:
			if (self.validate_position(move)) and \
				not (self.check_square_threatened([x, y],  \
					(int)(self.board[pos[0], pos[1]]))) and \
				((int) (self.board[x][y] / 10) != \
				(int)(self.board[move[0]][move[1]] / 10) or \
				self.board[move[0]][move[1]] == 0):
					valid_moves.append(move)

		# Castling
		if self.board[x, y] % 10 == 8:
			if self.board_start: # Playing black.
				NUM_LEFT = 2
				NUM_RIGHT = 3
			else: # Playing white.
				NUM_LEFT = 3
				NUM_RIGHT = 2
			i = 1
			while i < NUM_LEFT + 1:
				if (not self.board[x, y-i] == 0) or \
				 self.check_square_threatened([x, y-i],
				 	(int)(self.board[x, y] / 10)):
					break
				i += 1
			if i == NUM_LEFT + 1:
				if ((int) (self.board[x, y-i] / 10) == \
					(int) (self.board[x, y] / 10)) and \
					((int) (self.board[x, y-i] % 10) == 9):
						#valid_moves.append([x, y - i + NUM_LEFT-1])
						valid_moves.append([x, y - NUM_LEFT])
			else:
				print('i is: ', i)
			# Right castling
			i = 1
			while i < NUM_RIGHT + 1:
				if not self.board[x, y+i] == 0 or \
				self.check_square_threatened([x, y+i],
					(int)(self.board[x, y] / 10)):
					break
				i += 1
			if i == NUM_RIGHT + 1:
				if ((int) (self.board[x, y+i] / 10) == \
					(int) (self.board[x, y] / 10)) and \
					((int) (self.board[x, y+i] % 10) == 9):
					#valid_moves.append([x, y + i - NUM_RIGHT + 1])
					valid_moves.append([x, y + NUM_RIGHT])
		return valid_moves

	def get_queen_moves(self, pos):
		valid_moves = []
		valid_moves += self.get_bishop_moves(pos)
		valid_moves += self.get_rook_moves(pos)
		return valid_moves

	def get_bishop_moves(self, pos):
		valid_moves = []
		valid_moves += self.line_helper(pos, 8, 8, 1, 1, 1) 	# bottom right
		valid_moves += self.line_helper(pos, 8, 8, 1, -1, 1)	# bottom left
		valid_moves += self.line_helper(pos, 8, 8, -1, 1, 1)	# top right
		valid_moves += self.line_helper(pos, 8, 8, -1, -1, 1)	# top left
		return valid_moves

	def get_knight_moves(self, pos):
		moves  = []
		moves.append([pos[0] - 2, pos[1] - 1])
		moves.append([pos[0] - 2, pos[1] + 1])
		moves.append([pos[0] - 1, pos[1] - 2])
		moves.append([pos[0] - 1, pos[1] + 2])
		moves.append([pos[0] + 1, pos[1] - 2])
		moves.append([pos[0] + 1, pos[1] + 2])
		moves.append([pos[0] + 2, pos[1] - 1])
		moves.append([pos[0] + 2, pos[1] + 1])
		valid_moves = [move for move in moves if \
			(self.validate_position(move) and \
			(self.board[move[0], move[1]] == 0 or \
			(int)(self.board[move[0], move[1]] / 10) != \
			(int)(self.board[pos[0], pos[1]] / 10)))]
		return valid_moves

	def get_rook_moves(self, pos):
		valid_moves = []
		valid_moves += self.line_helper(pos, 8, 8, 0, 1, 1) 	# right
		valid_moves += self.line_helper(pos, 8, 8, 0, -1, 1) 	# left
		valid_moves += self.line_helper(pos, 8, 8, 1, 0, 1) 	# down
		valid_moves += self.line_helper(pos, 8, 8, -1, 0, 1) 	# up
		return valid_moves

	def get_pawn_moves(self, pos):
		valid_moves = []
		x = pos[0]
		y = pos[1]

		# Assign constants based on pawn type
		if self.board_start: # White start
			if (int) (self.board[x, y] / 10) == 0: # White
				ORIGINAL_ROW = 1
				FORWARD_I = 1
				EN_PASSANT_ROW = 4
			else: # Black
				ORIGINAL_ROW = 6
				FORWARD_I = -1
				EN_PASSANT_ROW = 3
		else: # Black start
			if (int) (self.board[x, y] / 10) == 0: # White
				ORIGINAL_ROW = 6
				FORWARD_I = -1
				EN_PASSANT_ROW = 3
			else:	# Black
				ORIGINAL_ROW = 1
				FORWARD_I = 1
				EN_PASSANT_ROW = 4

		# Initial double move
		if x == ORIGINAL_ROW:
			valid_moves += self.line_helper(pos, x + 3*FORWARD_I, 8,
				FORWARD_I, 0, 0)
		else:	# Normal single move
			valid_moves += self.line_helper(pos, x + 2*FORWARD_I, 8,
				FORWARD_I, 0, 0)

		# Check Diagonal Attacks
		valid_moves += self.line_helper(pos, x + FORWARD_I, y + 1, FORWARD_I,
			1, 1)
		valid_moves += self.line_helper(pos, x + FORWARD_I, y - 1, FORWARD_I,
			-1, 1)

		# En Passant Attack
		if x == EN_PASSANT_ROW:
			if self.validate_position([x, y-1]) and \
			   self.board[x, y-1] % 10 == 7:
			   		valid_moves += [x + FORWARD_I, y-1]
			if self.validate_position([x, y+1]) and \
				self.board[x, y+1] % 10 == 7:
					valid_moves += [x + FORWARD_I, y+1]
		return valid_moves

if __name__ == "__main__":
	board = Board()
