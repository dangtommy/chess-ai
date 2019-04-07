import pygame
from chess_board import Board

# Colors
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]
YELLOW = [255, 255, 0]

class Game:
    def __init__(self):
        pygame.display.init()
        self.running = True
        self.display = pygame.display.set_mode([BOARD_X, BOARD_Y])
        self.board = Board()
        self.selected_piece = None
        self.king_checked = False
        self.advancing_pawn = False

    # Handle inputs to the game board.
    def handle_key_event(self, e):

        # Pieces are selected, but did not press one.
        if self.selected_piece and not e in self.valid_moves:
            print("deselecting")
            self.selected = None
            self.valid_moves = None
            self.draw_board()

        # Advancing pawn.
        elif self.advancing_pawn:
            self.advancing_pawn = False

        # Position is a move.
        elif self.selected_piece and e in self.valid_moves:
            if self.king_checked:
                pass
            else:
                self.move_piece(self.get_piece(self.selected_piece[0],
                    self.selected_piece[1]), self.selected_piece[0],
                    self.selected_piece[1], e[0], e[1])
                self.selected_piece = None
                self.valid_moves = None
                self.draw_board()

        # Display piece's valid moves.
        else:
            self.selected_piece = e
            valid_moves = self.board.get_valid_moves_at_square(e[0], e[1])
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

    # Draws the board based on the current board array state.
    def draw_board(self):
        # Place the pieces on the board.
        # Draw the white/black tiles on the board.
        for i in range(0, 8):
            for j in range(0, 8):
                if not self.board[i, j] == 0:
                    if self.board[i, j] < 10: # White
                        pygame.draw.rect(self.display, BLUE,
                            [j * 64, i * 64, 64, 64], 0)
                    else:   # Black
                        pygame.draw.rect(self.display, GREEN,
                            [j * 64, i * 64, 64, 64], 0)
                else: # Draw empty tile.
                    tile_color = WHITE
                    if not (i+j) % 2 == 0:
                        tile_color = BLACK
                    pygame.draw.rect(self.display, tile_color, [j * 64,
                        i * 64, 64, 64], 0)

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
            elif new_y == 0 or new_y == 8: # Pawn advancement.
                self.board.update_square(orig_x, orig_y, 0)
                # TODO: Pawn advancement.
                # Currently just makes queens.
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
        # Draw options.
        pygame.draw.rect(self.display, YELLOW, [3 * 64, 3 * 64, 64, 64], 0)
        pygame.draw.rect(self.display, YELLOW, [3 * 64, 4 * 64, 64, 64], 0)
        pygame.draw.rect(self.display, YELLOW, [4 * 64, 3 * 64, 64, 64], 0)
        pygame.draw.rect(self.display, YELLOW, [4 * 64, 4 * 64, 64, 64], 0)

    # TODO: Determine if checkmate has been reached.
    # Should trigger when King square is threatened.
    def checked(self):
        pass

if __name__ == "__main__":
    game = Game()
    game.draw_board()
    game.loop()
