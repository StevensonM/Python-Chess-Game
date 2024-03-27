# Author: Matthew Stevenson
# GitHub username: StevensonM
# Date: 03/12/2024
# Description: Final Portfolio Project.

class ChessVar:
    """Class to represent a modified chess game where fairy pieces are allowed into the game. If either player's King is
    captured, the game is over."""

    def __init__(self):
        """The init method."""
        self._game_board = [
         ['wr', 'wN', 'wb', 'wk', 'wq', 'wb', 'wN', 'wr'],
         ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
         ['.', '.', '.', '.', '.', '.', '.', '.'],
         ['.', '.', '.', '.', '.', '.', '.', '.'],
         ['.', '.', '.', '.', '.', '.', '.', '.'],
         ['.', '.', '.', '.', '.', '.', '.', '.'],
         ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
         ['br', 'bn', 'bb', 'bk', 'bq', 'bb', 'bn', 'br']
         ]

        self._players = ['white', 'black']
        self._current_player = 0
        self._game_state = 'UNFINISHED'
        self._white_fairy_count = 0
        self._black_fairy_count = 0

    def get_game_state(self):
        """Returns the game state."""
        return self._game_state

    def print_board(self):
        """Prints the board."""
        for row in self._game_board:
            print(" ".join(row))
        print()

    def make_move(self, starting_pos, ending_pos):
        """Moves the chess piece. Takes two parameters: the starting position and the ending position of the chess piece."""

        if self._game_state != 'UNFINISHED':  # Checks to see if the game state is unfinished.
            return False

        from_col, from_row = ord(starting_pos[0]) - ord('a'), int(starting_pos[1]) - 1
        to_col, to_row = ord(ending_pos[0]) - ord('a'), int(ending_pos[1]) - 1

        if not self.check_square(from_col, from_row) or not self.check_square(to_col, to_row):
            return False

        if not self.move_allowed(from_col, from_row, to_col, to_row):
            return False

        piece = self._game_board[from_row][from_col]
        if not self.check_player_piece(piece):
            return False

        self._game_board[to_row][to_col] = piece
        self._game_board[from_row][from_col] = '.'

        chess_pieces = [piece for row in self._game_board for piece in row]
        # Compresses the whole chess board into a usable list, so we can find either King's and update the game state as needed.

        if 'bk' not in chess_pieces:  # Checks to see if black's King has been captured.
            self._game_state = 'WHITE_WON'

        if 'wk' not in chess_pieces:  # Checks to see if white's King has been captured.
            self._game_state = 'BLACK_WON'

        self._current_player = 1 - self._current_player  # Switches the player

        return True

    def check_square(self, col, row):
        """Makes sure the square a player wants to move to is actually on the board."""
        return 0 <= col < 8 and 0 <= row < 8

    def move_allowed(self, from_col, from_row, to_col, to_row):
        """Checks to see if the current chess piece is allowed to make the prescribed move."""
        piece = self._game_board[from_row][from_col]
        captured_piece = self._game_board[to_row][to_col]

        if captured_piece[0] == 'w' and self._current_player == 1:  # Ensures a black piece can capture a white one.
            return True

        if captured_piece[0] == 'b' and self._current_player == 0:  # Ensures a white piece can capture a black one.
            return True

        if (piece[0] == 'w' and captured_piece[0] == 'w') or (piece[0] == 'b' and captured_piece[0] == 'b'):
            return False

        if piece == '.':
            return False

        if piece[1] == 'k':  # King move logic
            if abs(to_col - from_col) <= 1 and abs(to_row - from_row) <= 1:
                return True

        elif piece[1] == 'q':  # Queen move logic
            if (from_col == to_col or from_row == to_row or
                    abs(to_col - from_col) == abs(to_row - from_row)):
                return True

        elif piece[1] == 'r':  # Rook move logic
            if from_col == to_col:  # Checks to see if there's something in the Rook's path (column)
                it = 1 if to_row > from_row else -1
                for square in range(from_row + it, to_row, it):
                    if self._game_board[square][from_col] != '.':
                        return False
                return True

            elif from_row == to_row:  # Checks to see if there's something in the Rook's path (row)
                it = 1 if to_col > from_col else -1
                for square in range(from_col + it, to_col, it):
                    if self._game_board[from_row][square] != '.':
                        return False
                return True
            else:
                return False

        elif piece[1] == 'b':  # Bishop move logic
            if abs(to_col - from_col) == abs(to_row - from_row):
                #  Checks to see if there's something in the Bishop's path by iterating over it.
                it_col = 1 if to_col > from_col else -1
                it_row = 1 if to_row > from_row else -1
                col, row = from_col + it_col, from_row + it_row
                while col != to_col and row != to_row:
                    if self._game_board[row][col] != '.':
                        return False
                    col += it_col
                    row += it_row
                return True

        elif piece[1] == 'N':  # White Knight move logic
            if (abs(to_col - from_col) == 2 and abs(to_row - from_row) == 1) or \
                    (abs(to_col - from_col) == 1 and abs(to_row - from_row) == 2):
                return True

        elif piece[1] == 'n':  # Black Knight move logic
            if (abs(to_col - from_col) == 2 and abs(to_row - from_row) == 1) or \
                    (abs(to_col - from_col) == 1 and abs(to_row - from_row) == 2):
                return True

        elif piece == 'wf':  # White falcon move logic
            if to_row > from_row and abs(to_col - from_col) == abs(to_row - from_row):  # Forward move logic
                # Iterates through the piece's forward move path to see if there's anything blocking it.
                it_col = 1 if to_col > from_col else -1
                it_row = 1 if to_row > from_row else -1
                col, row = from_col + it_col, from_row + it_row
                while col != to_col and row != to_row:
                    if self._game_board[row][col] != '.':
                        return False
                    col += it_col
                    row += it_row
                return True
            if from_row > to_row and (from_col == to_col or from_row == to_row):  # Backward move logic
                # Iterates through the piece's backward move path to see if there's anything blocking it.
                it = 1 if to_row > from_row else -1
                for square in range(from_row + it, to_row, it):
                    if self._game_board[square][from_col] != '.':
                        return False
                return True

        elif piece == 'bf':  # Black falcon move logic
            if to_row < from_row and abs(to_col - from_col) == abs(to_row - from_row):  # Forward move logic
                # Iterates through the piece's forward move path to see if there's anything blocking it.
                it_col = 1 if to_col > from_col else -1
                it_row = 1 if to_row > from_row else -1
                col, row = from_col + it_col, from_row + it_row
                while col != to_col and row != to_row:
                    if self._game_board[row][col] != '.':
                        return False
                    col += it_col
                    row += it_row
                return True
            if to_row > from_row and (from_col == to_col or from_row == to_row):  # Backward move logic
                # Iterates through the piece's backward move path to see if there's anything blocking it.
                it = 1 if to_row > from_row else -1
                for square in range(from_row + it, to_row, it):
                    if self._game_board[square][from_col] != '.':
                        return False
                return True

        elif piece == 'wh':  # White hunter move logic
            if to_row > from_row and (from_col == to_col or from_row - to_row == 1):  # Forward move logic.
                it = 1 if to_row > from_row else -1
                for square in range(from_row + it, to_row, it):
                    if self._game_board[square][from_col] != '.':
                        return False
                return True
            if to_row < from_row and abs(to_col - from_col) == abs(to_row - from_row):  # Backward move logic
                it_col = 1 if to_col > from_col else -1
                it_row = 1 if to_row > from_row else -1
                col, row = from_col + it_col, from_row + it_row
                while col != to_col and row != to_row:
                    if self._game_board[row][col] != '.':
                        return False
                    col += it_col
                    row += it_row
                return True

        elif piece == 'bh':  # Black hunter move logic
            if to_row < from_row and (from_col == to_col or to_row - from_row == 1):  # Forward move logic
                it = 1 if to_row > from_row else -1
                for square in range(from_row + it, to_row, it):
                    if self._game_board[square][from_col] != '.':
                        return False
                return True

            if to_row > from_row and abs(to_col - from_col) == abs(to_row - from_row):  # Backward move logic
                it_col = 1 if to_col > from_col else -1
                it_row = 1 if to_row > from_row else -1
                col, row = from_col + it_col, from_row + it_row
                while col != to_col and row != to_row:
                    if self._game_board[row][col] != '.':
                        return False
                    col += it_col
                    row += it_row
                return True

        elif piece[1] == 'p':  # Pawn move logic
            if from_col == to_col:
                if self.empty_square_check(to_row, to_col):
                    if self._current_player == 0:
                        if from_row == 1:
                            return to_row == from_row + 1 or to_row == from_row + 2  # Allow pawn to move 2 squares its first move
                        else:
                            return to_row == from_row + 1
                    else:
                        if from_row == 6:
                            return to_row == from_row - 1 or to_row == from_row - 2  # Allows pawn to move 2 squares its first move
                        else:
                            return to_row == from_row - 1
                else:
                    return False

            elif abs(to_col - from_col) == 1 and abs(to_row - from_row) == 1:  # Allows pawn to capture diagonally
                if self._current_player == 0:
                    return self.check_black_piece(captured_piece)
                else:
                    return self.check_white_piece(captured_piece)
            else:
                return False
        return False

    def fairy_helper(square):
        """Converts the str into valid coordinates for the enter_fairy_piece function."""
        column, row = square
        row = int(row)

        assert "a" <= column <= "h"
        assert 1 <= row <= 8

        return row - 1, ord(column) - 97

    def enter_fairy_piece(self, piece_type, square):
        """Puts the fairy piece onto the board under various conditions."""
        row, column = ChessVar.fairy_helper(square)

        if piece_type not in ['wf', 'bf', 'wh', 'bh']:  # Makes sure the player can only enter a falcon or a hunter
            return False

        if self._game_state != 'UNFINISHED':
            return False

        if not (
                0 <= row < 2) and self._current_player == 0:  # Makes sure a player can only put the piece in their first two rows.
            return False

        if not (
                6 <= row < 8) and self._current_player == 1:  # Makes sure a player can only put the piece in their first two rows.
            return False

        if self.empty_square_check(row, column):
            if self._current_player == 0:
                if self._white_fairy_count >= 2:  # Makes sure white can only enter two fairy pieces.
                    return False
                self._white_fairy_count += 1
                if piece_type in [piece for row in self._game_board for piece in row]:  # Makes sure white can't enter a duplicate fairy piece.
                    return False
                lost_pieces = ['wq', 'wr', 'wb', 'wN']

            else:
                if self._black_fairy_count >= 2:  # Makes sure black can only enter two fairy pieces.
                    return False
                self._black_fairy_count += 1
                if piece_type in [piece for row in self._game_board for piece in row]:  # Makes sure black can't enter a duplicate fairy piece.
                    return False
                lost_pieces = ['bq', 'br', 'bb', 'bn']

            if any(piece in lost_pieces for row in self._game_board for piece in row):
                self._game_board[row][column] = piece_type
                self._current_player = 1 - self._current_player
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        """Formats string representation for printing."""
        return "\n".join(" ".join(f"{c:^4}" for c in row) for row in self._game_board)

    def empty_square_check(self, row, col):
        """Checks to see if a square is empty."""
        return self._game_board[row][col] == '.'

    def check_white_piece(self, piece):
        """Checks to see if a piece is white."""
        return piece[0] == 'w'

    def check_black_piece(self, piece):
        """Checks to see if a piece is black."""
        return piece[0] == 'b'

    def check_player_piece(self, piece):
        """Makes sure the piece actually belongs to the player."""
        return piece[0] == self._players[self._current_player][0]