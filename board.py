import pygame, numpy as np

# Constants for the board representation.

# Colors
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]
YELLOW = [255, 255, 0]

# Pieces
WHITE_KING = 1
WHITE_QUEEN = 2
WHITE_BISHOP = 3
WHITE_KNIGHT = 4
WHITE_ROOK = 5
WHITE_PAWN = 6  

BLACK_KING = 11
BLACK_QUEEN = 12
BLACK_BISHOP = 13
BLACK_KNIGHT = 14
BLACK_ROOK = 15
BLACK_PAWN = 16

# Positions
BOARD_X = 512
BOARD_Y = 512
class Game:
    def __init__(self):
        pygame.display.init()
        self.running = True 
        self.board = np.zeros([8,8])
        # TODO: Care, might have to switch this.
        self.display = pygame.display.set_mode([BOARD_X, BOARD_Y])
        self.init_game()
        print(str(self.board))
        self.selected = None
        self.valid_moves = None

    def init_game(self):
        # White pieces
        self.board[7, 4] = WHITE_KING
        self.board[7, 3] = WHITE_QUEEN
        self.board[7, 2] = self.board[7,5] = WHITE_BISHOP
        self.board[7, 1] = self.board[7,6] = WHITE_KNIGHT
        self.board[7, 0] = self.board[7,7] = WHITE_ROOK
        self.board[6,:] = WHITE_PAWN

        # Black pieces
        self.board[0, 3] = BLACK_KING
        self.board[0, 4] = BLACK_QUEEN
        self.board[0, 2] = self.board[0, 5] = BLACK_BISHOP
        self.board[0, 1] = self.board[0, 6] = BLACK_KNIGHT
        self.board[0, 0] = self.board[0, 7] = BLACK_ROOK
        self.board[1,:] = BLACK_PAWN

    # TODO:
    #   Add functionality to handle figuring out what piece was pressed
    #   Show valid moves for each type of piece, depending on what's on the board
    #   Execute valid moves
    def handle_key_event(self, e):
        
        # Pieces are selected, but did not press one
        if self.selected and not e in self.valid_moves:
            print("deselecting")
            self.selected = None
            self.valid_moves = None
            self.draw_board()

        # Position is a move
        elif self.selected and e in self.valid_moves:
            self.board[e[0], e[1]] = self.board[self.selected[0], self.selected[1]]
            self.board[self.selected[0], self.selected[1]] = 0
            self.selected = None
            self.valid_moves = None 
            self.draw_board()
            
        # TODO: switch/case
        # TODO: pos is king
        elif self.board[e[0], e[1]] % 10 == 1:
            self.selected = e
            self.valid_moves = self.get_king_moves(e)
            self.draw_board()
        # TODO: pos is Queen
        elif self.board[e[0], e[1]] % 10 == 2:
            self.selected = e
            self.valid_moves = self.get_queen_moves(e)
            self.draw_board()

        # TODO: pos is Bishop
        elif self.board[e[0],e[1]] % 10 == 3:
            self.selected = e
            self.valid_moves = self.get_bishop_moves(e)
            self.draw_board()

        # TODO: pos is Knight

        # TODO: pos is Rook
        elif self.board[e[0], e[1]] % 10 == 5:
            self.selected = e
            self.valid_moves = self.get_rook_moves(e)
            self.draw_board()

        # Pos is Pawn
        elif self.board[e[0], e[1]] % 10 == 6:
            self.selected = e
            self.valid_moves = self.get_pawn_moves(e)
            self.draw_board()

        pygame.display.update()
        print(str(self.board))

    def draw_board(self):
        # Place the pieces on the board.
        # Draw the white/black tiles on the board.
        for i in range(0, 8):
            for j in range(0, 8):
                if not self.board[i,j] == 0:
                    # White
                    if self.board[i,j] < 10:
                        #print("drawing BLUE on " + str([i, j]))
                        pygame.draw.rect(self.display, BLUE, [j * 64, i * 64, 64, 64], 0)
                    else:
                        #print("drawing GREEN on " + str([i, j]))
                        pygame.draw.rect(self.display, GREEN, [j * 64, i * 64, 64, 64], 0)
                else:
                    tile_color = WHITE
                    if not (i+j) % 2 == 0:
                        tile_color = BLACK
                    #print("drawing on " + str([i, j]))
                    pygame.draw.rect(self.display, tile_color, [j * 64, i * 64, 64, 64], 0)

        # Draw moves if a piece has been selected.
        if self.selected:
            for move in self.valid_moves:
                print("move: " + str(move))
                move_color = None
                if self.board[move[0], move[1]] == 0:
                    move_color = YELLOW
                else:
                    move_color = RED
                pygame.draw.rect(self.display, move_color, [move[1] * 64, move[0] * 64, 64, 64], 0)
        pygame.display.update()

    def loop(self):
        #TODO: Run the game here.
        while self.running:
            for event in pygame.event.get():

                # Shuts down the game.
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("pos: " + str(event.pos))
                    tile = [event.pos[1] // 64, event.pos[0] // 64]
                    print("square pos: " + str(tile))
                    self.handle_key_event(tile)

    def validate_position(self, pos):
        if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7:
            print("TRUE for pos: " + str(pos))
            return True
            print("FALSE for pos: " + str(pos))
        return False

# Get valid moves for each piece.

    #TODO: have to consider tiles that are "under threat" and prevent those.
    def get_king_moves(self, pos):
        valid_moves = []
        for i in range(pos[0] - 1, pos[0] + 2):
            for j in range(pos[1] - 1, pos[1] + 2):
                print("i: " + str(i) + " j: " + str(j))
                if self.validate_position([i, j]) and not self.board[i, j] % 10 == 1:
                    if self.board[pos[0], pos[1]] < 10 and not 0 < self.board[i, j] < 10 or \
                        self.board[pos[0], pos[1]] > 10 and not self.board[i, j] > 10:
                            valid_moves.append([i, j])
        return valid_moves

    #TODO
    def get_queen_moves(self, pos):
        valid_moves = []
        valid_moves += self.line_helper(pos, -1, 0, -1, 0)
        valid_moves += self.line_helper(pos, 1, 0, 1, 0)
        valid_moves += self.line_helper(pos, 0, -1, 0, -1)
        valid_moves += self.line_helper(pos, 0, 1, 0, 1)
        valid_moves += self.line_helper(pos, -1, -1, -1, -1)
        valid_moves += self.line_helper(pos, -1, 1, -1, 1)
        valid_moves += self.line_helper(pos, 1, -1, 1, -1)
        valid_moves += self.line_helper(pos, 1, 1,1, 1)
        return valid_moves

    #TODO
    def get_bishop_moves(self, pos):
        valid_moves = []
        valid_moves += self.line_helper(pos, -1, -1, -1, -1)
        valid_moves += self.line_helper(pos, -1, 1, -1, 1)
        valid_moves += self.line_helper(pos, 1, -1, 1, -1)
        valid_moves += self.line_helper(pos, 1, 1,1, 1)
        return valid_moves

    #TODO
    def get_knight_moves(self, pos):
        pass

    #TODO
    def get_rook_moves(self, pos):
        valid_moves = []
        valid_moves += self.line_helper(pos, -1, 0, -1, 0)
        valid_moves += self.line_helper(pos, 1, 0, 1, 0)
        valid_moves += self.line_helper(pos, 0, -1, 0, -1)
        valid_moves += self.line_helper(pos, 0, 1, 0, 1)
        print("ROOK valid moves: " + str(valid_moves))
        return valid_moves

    def line_helper(self, pos, i_offset, j_offset, i_inc, j_inc):
        valid_moves = []
        while self.validate_position([pos[0] + i_offset, pos[1] + j_offset]) \
            and self.board[pos[0] + i_offset, pos[1] + j_offset] == 0:
            valid_moves.append([pos[0] + i_offset, pos[1] + j_offset])
            i_offset += i_inc
            j_offset += j_inc
        if self.validate_position([pos[0] + i_offset, pos[1] + j_offset]):
            if abs(self.board[pos[0] + i_offset, pos[1] + j_offset]) - abs(self.board[pos[0], pos[1]]) > 5:
                valid_moves.append([pos[0] + i_offset, pos[1] + j_offset])
        return valid_moves

    #TODO
    def get_pawn_moves(self, pos):
        moves = []
        attacks = []
        valid_moves = []

        # Black pawn
        if self.board[pos[0], pos[1]] > 10:
            moves.append([pos[0] + 1, pos[1]])
            for i in (-1, 1):
                attacks.append([pos[0] + 1, pos[1] + i])

        # White pawn
        else:
            moves.append([pos[0] - 1, pos[1]])
            for i in (-1, 1):
                attacks.append([pos[0] - 1, pos[1] + i])

        # Validate moves
        for move in moves:
            if self.validate_position(move) and self.board[move[0], move[1]] == 0:
                valid_moves.append(move)
        for attack in attacks:
            if self.validate_position(attack):
                if self.board[self.selected[0], self.selected[1]] < 10:
                    if self.board[attack[0], attack[1]] > 10:
                        print("first if")
                        valid_moves.append(attack)
                elif 0 < self.board[attack[0], attack[1]] < 10:
                    print("second if")
                    print("selected = " + str(self.selected))
                    valid_moves.append(attack)
        print("PAWN valid moves: " + str(valid_moves))
        return valid_moves


if __name__== "__main__":
    game = Game()
    game.draw_board()
    game.loop()
