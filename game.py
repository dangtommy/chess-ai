import pygame
from chess_board import Board

# Colors
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]
YELLOW = [255, 255, 0]

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
        self.advancing_pawn = False
        self.valid_moves = []

    # TODO: Fix this to give instructions for pawn advancement.
    def draw_text(self):
        instructions = pygame.font.render('Press enter to quit game.', 1, WHITE)
        self.display.blit(instructions, (576, 100))

    # Handle inputs to the game board.
    def handle_key_event(self, e):

        if e[0] > 7 or e[1] > 7:
            return

        # Pieces are selected, but did not press one.
        if self.selected_piece and not e in self.valid_moves:
            print("deselecting")
            self.selected_piece = None
            self.valid_moves = []
            self.draw_board()

        # Advancing pawn.
        elif self.advancing_pawn:
            print('advancing pawn')
            self.advancing_pawn = False

        # Position is a move.
        elif self.selected_piece and e in self.valid_moves:
            print('moving')
            if self.king_checked:
                pass
            else:
                self.move_piece(self.board.get_piece(self.selected_piece[0],
                    self.selected_piece[1]), self.selected_piece[0],
                    self.selected_piece[1], e[0], e[1])
                self.selected_piece = None
                self.valid_moves = []
                self.draw_board()

        # Display piece's valid moves.
        else:
            print('display valid moves')
            print('valid moves before: ', self.valid_moves)
            self.selected_piece = e
            print(str(self.board.board))
            self.valid_moves = self.board.get_valid_moves_at_square(e[0], e[1])
            print('valid moves: ', self.valid_moves)
            self.draw_board()

    # Game loop logic.
    # TODO:
    # - Add background info squares.
    # - Handle pawn advancement.
    def loop(self):
        while self.running:
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

    # Draws the board based on the current board array state.
    def draw_board(self):
        # Place the pieces on the board.
        # Draw the white/black tiles on the board.
        for i in range(0, 8):
            for j in range(0, 8):
                if not self.board.get_piece(i, j) == 0:
                    if self.board.get_piece(i, j) < 10: # White
                        pygame.draw.rect(self.display, BLUE, \
                            [j * 64, i * 64, 64, 64], 0)
                    else:   # Black
                        pygame.draw.rect(self.display, GREEN, \
                            [j * 64, i * 64, 64, 64], 0)
                else: # Draw empty tile.
                    tile_color = WHITE
                    if not (i+j) % 2 == 0:
                        tile_color = BLACK
                    pygame.draw.rect(self.display, tile_color, [j * 64, \
                        i * 64, 64, 64], 0)

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

	# Make a move. Check for special moves here.
    def move_piece(self, piece, orig_x, orig_y, new_x, new_y):
		# Handle castling.
        if piece % 10 == 8:
            offset = orig_x - new_x # pos: left, neg: right
            if abs(offset) > 1:
                print("Castling")
                # King update
                self.board.update_square(orig_x, orig_y, 0)
                self.board.update_square(new_x, new_y, piece-7)
                # Rook update
                self.board.update_square(new_x + offset, new_y, \
                    piece + 4)
                self.board.update_square(new_x - offset, new_y, 0)
            else:
                self.board.update_square(orig_x, orig_y, 0)
                self.board.update_square(new_x, new_y, piece)
        # Handle rook rename if not castling.
        elif piece % 10 == 9:
        	self.board.update_square(orig_x, orig_y, 0)
        	self.board.update_square(new_x, new_y, piece - 4)

        # Handle special pawn behavior.
        elif piece % 10 == 6:
            offset = orig_y - new_y
            if abs(offset) > 1: # First move.
                self.board.update_square(orig_x, orig_y, 0)
                self.board.update_square(new_x, new_y, piece + 1)
            elif new_x == 0 or new_x == 7: # Pawn advancement.
                self.board.update_square(orig_x, orig_y, 0)
                # TODO: Pawn advancement.
                # Currently just makes queens.
                self.draw_advancement_choice()
                new_piece = piece - 4
                self.board.update_square(new_x, new_y, new_piece)
            else: # Normal pawn behavior.
                self.board.update_square(orig_x, orig_y, 0)
                self.board.update_square(new_x, new_y, piece)

        # Handle returning en passant pawn to regular pawn.
        elif piece % 10 == 7:
            self.board.update_square(orig_x, orig_y, 0)
            self.board.update_square(new_x, new_y, piece - 1)
        else: # Normal behavior.
            self.board.update_square(orig_x, orig_y, 0)
            self.board.update_square(new_x, new_y, piece)

    # TODO: When pawn advances, draw
    def draw_advancement_choice(self):
        print('drawing options')
        # Draw options.
        pygame.draw.rect(self.display, YELLOW, [3 * 64, 3 * 64, 64, 64], 0)
        pygame.draw.rect(self.display, YELLOW, [3 * 64, 4 * 64, 64, 64], 0)
        pygame.draw.rect(self.display, YELLOW, [4 * 64, 3 * 64, 64, 64], 0)
        pygame.draw.rect(self.display, YELLOW, [4 * 64, 4 * 64, 64, 64], 0)
        # Update board surface.
        pygame.display.update()

    # TODO: Determine if checkmate has been reached.
    # Should trigger when King square is threatened.
    def checked(self, pos):
        for threat in (self.board.get_threat_board())[pos[0]][pos[1]]:
            if not (int) (threat / 10) == \
                (int) (self.get_piece(pos[0], pos[1]) / 10):
                return True
        return False

if __name__ == "__main__":
    game = Game()
    game.draw_board()
    game.loop()
