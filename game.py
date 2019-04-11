import pygame, copy
from chess_board import Board

# Colors
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]
YELLOW = [255, 255, 0]
GRAY = [170, 172, 175]

# Positions
BOARD_X = 512 + 256
BOARD_Y = 512

class Game:
    def __init__(self):

        # Board.
        pygame.display.init()
        self.running = True
        self.display = pygame.display.set_mode([BOARD_X, BOARD_Y])
        self.board = Board()

        # Text - instructions and help messages.
        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 30)

        # Input / game logic variables.
        self.selected_piece = None
        self.king_checked = False
        self.valid_moves = []
        self.turn = 0
        self.game_over = False

    '''
    Drawing
    '''

    # Draws the board based on the current board array state.
    def draw_board(self):
        # Place the pieces on the board.
        # Draw the white/black tiles on the board.
        for i in range(0, 8):
            for j in range(0, 8):
                # Draw board.
                tile_color = WHITE
                if not (i+j) % 2 == 0:
                    tile_color = GRAY
                pygame.draw.rect(self.display, tile_color, [j * 64, \
                    i * 64, 64, 64], 0)

                # Draw appropriate piece.
                piece = self.board.get_piece(i, j)
                if not piece == 0:
                    #if self.board.get_piece(i, j) < 10: # White
                    #    pygame.draw.rect(self.display, BLUE, \
                    #        [j * 64, i * 64, 64, 64], 0)
                    #else:   # Black
                    #    pygame.draw.rect(self.display, GREEN, \
                    #        [j * 64, i * 64, 64, 64], 0)

                    # Draw King
                    if piece % 10 == 1 or piece % 10 == 8:
                        self.draw_king((int)(piece / 10), i, j)

                    # Draw Queen
                    elif piece % 10 == 2:
                        self.draw_queen((int)(piece / 10), i, j)

                    # Draw Bishop
                    elif piece % 10 == 3:
                        self.draw_bishop((int)(piece / 10), i, j)

                    # Draw Knight
                    elif piece % 10 == 4:
                        self.draw_knight((int)(piece / 10), i, j)

                    # Draw Rook
                    elif piece % 10 == 5 or piece % 10 == 9:
                        self.draw_rook((int)(piece / 10), i, j)
                    # Draw pawn
                    elif piece % 10 == 6 or piece % 10 == 7:
                        self.draw_pawn((int)(piece / 10), i, j)

        # Draw moves if a piece has been selected.
        if self.selected_piece and len(self.valid_moves) > 0:
            for move in self.valid_moves:
                print("move: ", str(move))
                move_color = None
                if self.board.get_piece(move[0], move[1]) == 0:
                    move_color = YELLOW
                else:
                    move_color = RED
                pygame.draw.rect(self.display, move_color, [move[1] * 64, \
                    move[0] * 64, 64, 64], 0)

        # Draw text.
        self.draw_text()

        # Update board surface.
        pygame.display.update()

    # TODO: Fix this to give instructions for pawn advancement.
    def draw_text(self):
        pass
        #instructions = pygame.font.render('Press enter to quit game.', 1, WHITE)
        #self.display.blit(instructions, (576, 100))

    # TODO: Drawing functions for each of the pieces, rather than green adn blue.

    # Draws a king on the board.
    def draw_king(self, player, i, j):
        if 1 - player:
            main_color = BLUE
        else:
            main_color = GREEN

        # cross
        pygame.draw.rect(self.display, main_color, [j * 64 + 28, i * 64 + 4, 4, 8], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 24, i * 64 + 8, 12, 2], 0)
        # body
        pygame.draw.rect(self.display, main_color, [j * 64 + 22, i * 64 + 12, 16, 20], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 20, i * 64 + 16, 20, 12], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 18, i * 64 + 18, 24, 8], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 24, i * 64 + 32, 12, 20], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 20, i * 64 + 52, 20, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 16, i * 64 + 56, 28, 4], 0)
    # Draws a queen on the board.
    def draw_queen(self, player, i, j):
        if 1 - player:
            main_color = BLUE
        else:
            main_color = GREEN
        # crown
        pygame.draw.rect(self.display, main_color, [j * 64 + 28, i * 64 + 4, 4, 8], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 20, i * 64 + 8, 4, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 36, i * 64 + 8, 4, 4], 0)

        # body
        pygame.draw.rect(self.display, main_color, [j * 64 + 22, i * 64 + 12, 16, 20], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 20, i * 64 + 16, 20, 12], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 18, i * 64 + 18, 24, 8], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 24, i * 64 + 32, 12, 20], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 20, i * 64 + 52, 20, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 16, i * 64 + 56, 28, 4], 0)

    # Draws a bishop on the board.
    def draw_bishop(self, player, i, j):
        if 1 - player:
            main_color = BLUE
        else:
            main_color = GREEN

        pygame.draw.rect(self.display, main_color, [j * 64 + 30, i * 64 + 8, 4, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 28, i * 64 + 12, 4, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 26, i * 64 + 16, 4, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 26, i * 64 + 20, 12, 20], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 34, i * 64 + 16, 4, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 34, i * 64 + 12, 2, 4], 0)

        pygame.draw.rect(self.display, main_color, [j * 64 + 20, i * 64 + 28, 24, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 24, i * 64 + 32, 16, 20], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 20, i * 64 + 48, 24, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 16, i * 64 + 52, 32, 4], 0)

    # Draws a knight on the board.
    def draw_knight(self, player, i, j):
        if 1 - player:
            main_color = BLUE
        else:
            main_color = GREEN

        pygame.draw.rect(self.display, main_color, [j * 64 + 24, i * 64 + 8, 20, 8], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 20, i * 64 + 16, 32, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 16, i * 64 + 20, 36, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 12, i * 64 + 24, 40, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 8, i * 64 + 28, 44, 8], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 8, i * 64 + 36, 16, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 32, i * 64 + 36, 20, 8], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 28, i * 64 + 44, 24, 8], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 24, i * 64 + 52, 24, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 16, i * 64 + 56, 36, 4], 0)

    # Draws a rook on the board.
    def draw_rook(self, player, i, j):
        if 1 - player:
            main_color = BLUE
        else:
            main_color = GREEN
        pygame.draw.rect(self.display, main_color, [j * 64 + 17, i * 64 + 16, 6, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 29, i * 64 + 16, 6, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 41, i * 64 + 16, 6, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 17, i * 64 + 20, 30, 12], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 22, i * 64 + 32, 20, 24], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 17, i * 64 + 48, 30, 8], 0)

    # Draws a pawn on the board.
    def draw_pawn(self, player, i, j):
        if 1 - player:
            main_color = BLUE
        else:
            main_color = GREEN
        pygame.draw.rect(self.display, main_color, [j * 64 + 30, i * 64 + 12, 4, 16], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 28, i * 64 + 14, 8, 12], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 26, i * 64 + 16, 12, 8], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 24, i * 64 + 18, 16, 4], 0)

        pygame.draw.rect(self.display, main_color, [j * 64 + 20, i * 64 + 32, 24, 4], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 24, i * 64 + 36, 16, 16], 0)
        pygame.draw.rect(self.display, main_color, [j * 64 + 16, i * 64 + 52, 32, 4], 0)

    '''
    Game logic
    '''

    # Game loop logic.
    # TODO:
    # - Add background info squares.
    # - Turn logic.
    def loop(self):
        while self.running:
            if self.game_over:
                for event in pygame.event.get():

                    # Restarts the game.
                    if event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_r:
                        # Input / game logic variables.
                        self.restart_game()
            else:
                for event in pygame.event.get():

                    # Shuts down the game.
                    if event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_RETURN:
                        self.running = False

                    # Handle key event to the game board.
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        tile = [event.pos[1] // 64, event.pos[0] // 64]
                        self.handle_key_event(tile)

                    # Show threat board.
                    if event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_LEFT:
                        tb = self.board.get_threat_board()
                        print('threat board: ')
                        for row in range(0, 8):
                            for col in range(0, 8):
                                print(tb[row][col])

                    # Restarts the game.
                    if event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_r:
                        self.restart_game()
    def restart_game(self):
        self.board.init_board()
        self.selected_piece = None
        self.valid_moves = []
        self.turn = 0
        self.game_over = False
        self.draw_board()

    # Handle inputs to the game board.
    def handle_key_event(self, e):

        # Prevent any action from happening on the right side of the board.
        if e[0] > 7 or e[1] > 7:
            return

        # Pieces are selected, but did not press one.
        if self.selected_piece and not e in self.valid_moves:
            print("deselecting")
            self.selected_piece = None
            self.valid_moves = []
            self.draw_board()

        # Position is a move.
        elif self.selected_piece and e in self.valid_moves:
            print('moving')
            # TODO: Prevent the move if the king would continue to be checked.
            if self.check_king(self.board):
                print('king checked.')
                potential_board = copy.deepcopy(self.board)
                self.move_piece(potential_board,
                    self.board.get_piece(self.selected_piece[0],
                    self.selected_piece[1]), self.selected_piece[0],
                    self.selected_piece[1], e[0], e[1])
                if self.check_king(potential_board):
                    print(' still checked.')
                else:
                    self.move_piece(self.board,
                        self.board.get_piece(self.selected_piece[0],
                        self.selected_piece[1]), self.selected_piece[0],
                        self.selected_piece[1], e[0], e[1])
                    self.selected_piece = None
                    self.valid_moves = []
                    self.draw_board()
                    self.turn = 1 - self.turn
                    checked_pos = self.check_king(self.board)
                    if checked_pos and self.check_for_mate(checked_pos):
                        self.game_over = True
            # TODO: Evaluate opposite king checked?
            else:
                self.move_piece(self.board,
                    self.board.get_piece(self.selected_piece[0],
                    self.selected_piece[1]), self.selected_piece[0],
                    self.selected_piece[1], e[0], e[1])
                self.selected_piece = None
                self.valid_moves = []
                self.draw_board()
                self.turn = 1 - self.turn
                checked_pos = self.check_king(self.board)
                if checked_pos and self.check_for_mate(checked_pos):
                    self.game_over = True

        # Display piece's valid moves.
        else:
            # Allow the selected piece to move if it corresponds to this turn.
            if (int) (self.board.get_piece(e[0], e[1]) / 10) == self.turn:
                print('selected_piece: ', self.board.get_piece(e[0], e[1]))
                self.selected_piece = e
                print(str(self.board.board))
                self.valid_moves = \
                    self.board.get_valid_moves_at_square(e[0], e[1])
                self.draw_board()
            else:
                print('invalid selection.')

    # Let the user advance their pawn using the keys 1 - 4.
    def get_advancement_choice(self, color):
        choice = None
        while choice == None:
            for event in pygame.event.get():

                # Advance to queen.
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    choice = (color * 10) + self.board.WHITE_QUEEN

                # Advance to bishop.
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    choice = (color * 10) + self.board.WHITE_BISHOP

                # Advance to knight.
                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    choice = (color * 10) + self.board.WHITE_KNIGHT

                # Advance to rook.
                if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    choice = (color * 10) + self.board.WHITE_ROOK
        return choice

    # Resolve if the King of the current player is checked.
    def check_king(self, board):
        for i in range(0, 8):
            for j in range(0, 8):
                piece = board.get_piece(i, j)
                # Real logic
                if (piece % 10 == board.WHITE_KING \
                or piece % 10 == board.WHITE_FIRST_KING) \
                and (int) (board.get_piece(i, j) / 10) == self.turn:
                    if board.check_square_threatened([i, j], self.turn):
                        print('king checked')
                        return [i, j]
        print('king not checked')
        return None

    # Check if the King is checkmated.
    # Make a copy of the board and try to execute all moves. If there exists a
    # move that would place the king not in check, then return false. Else,
    # return true.
    def check_for_mate(self, pos):
        for i in range(0, 8):
            for j in range(0, 8):
                if (int) (self.board.get_piece(i, j) / 10) == self.turn:
                    moves = self.board.get_valid_moves_at_square(i, j)
                    print('orig: ', i, ', ', j)
                    for move in moves:
                        print('move: ', move)
                        check_board = copy.deepcopy(self.board)
                        self.move_piece(check_board,
                            check_board.get_piece(i, j), i, j, move[0], move[1])
                        print(str(check_board.board))
                        if not self.check_king(check_board):
                            return False
                        print(' king still checked with this move')
        print('checkmate')
        return True

    # TODO: Add an argument for new_piece, the pawn advancement replacement.
    # This will make it easier to pass in pawn advancement AI move choices.

	# Make a move. Check for special moves here.
    def move_piece(self, board, piece, orig_x, orig_y, new_x, new_y):
		# Handle castling.
        print('in move piece')
        if piece % 10 == 8:
            offset = orig_y - new_y # pos: left, neg: right
            if abs(offset) > 1:
                # King update
                board.update_square(orig_x, orig_y, 0)
                board.update_square(new_x, new_y, piece - 7)
                # Rook update
                board.update_square(new_x, new_y + offset/(abs(offset)), \
                    10*(int)(piece / 10) + self.board.WHITE_ROOK)
                board.update_square(new_x, new_y - offset/(abs(offset)), 0)
            else:
                board.update_square(orig_x, orig_y, 0)
                board.update_square(new_x, new_y, piece)
        # Handle rook rename if not castling.
        elif piece % 10 == 9:
        	board.update_square(orig_x, orig_y, 0)
        	board.update_square(new_x, new_y, piece - 4)

        # Handle special pawn behavior.
        elif piece % 10 == 6:
            offset = orig_y - new_y
            if abs(offset) > 1: # First move.
                board.update_square(orig_x, orig_y, 0)
                board.update_square(new_x, new_y, piece + 1)
            elif new_x == 0 or new_x == 7: # Pawn advancement.
                new_piece = self.get_advancement_choice((int)(piece / 10))
                board.update_square(orig_x, orig_y, 0)
                board.update_square(new_x, new_y, new_piece)
            else: # Normal pawn behavior.
                board.update_square(orig_x, orig_y, 0)
                board.update_square(new_x, new_y, piece)

        # Handle returning en passant pawn to regular pawn.
        elif piece % 10 == 7:
            board.update_square(orig_x, orig_y, 0)
            board.update_square(new_x, new_y, piece - 1)
        else: # Normal behavior.
            board.update_square(orig_x, orig_y, 0)
            board.update_square(new_x, new_y, piece)
        board.update_threats()

if __name__ == "__main__":
    game = Game()
    game.draw_board()
    game.loop()
