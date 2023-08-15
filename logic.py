"""Handles the game's logic."""

from itertools import cycle
from typing import NamedTuple

BOARD_ROWS = 6
"""The number of rows in the board."""
BOARD_COLUMNS = 7
"""The number of columns in the board."""


class Player(NamedTuple):
    """Represents a player and their ID and colour."""

    # TODO: maybe add constructor to force id to be a positive integer to prevent clashes with Square.NO_PIECE

    id: int
    """The id of the player, e.g. 1 or 2. Should be a positive integer."""
    colour: str
    """The colour of the player's pieces."""


class Square(NamedTuple):
    """Represents a square in the board and if a player has placed a piece in it."""

    NO_PIECE = -1
    """Used to indicate that the square has no piece in it."""

    row: int
    """The row of the square in the board."""
    column: int
    """The column of the square in the board."""
    piece_id: int = NO_PIECE
    """The id of the player who placed a piece in the square. The value NO_PIECE means there is no piece in the square."""


PLAYERS = (
    Player(id=1, colour="blue"),
    Player(id=2, colour="red"),
)
"""The players in the game."""


class Logic:
    """The game's logic."""

    def __init__(self):
        """Initializes the game's logic."""
        self._players = cycle(PLAYERS)
        """The players in the game, in a cycle."""
        self._current_squares: list[list[Square]] = []
        """A list with all of the squares in the board, in the form [row][column]."""
        self._has_winner: bool = False
        """Used to determine if the game has a winner."""
        self.current_player: Player = next(self._players)
        """The player whose turn it is."""

        self._initialize_board()

    def _initialize_board(self):
        """Initialize all of the squares in the board, in the form [row][column]."""
        self._current_squares = [[Square(row, column) for column in range(BOARD_COLUMNS)] for row in range(BOARD_ROWS)]

    def get_first_empty_square_in_column(self, column: int) -> Square | None:
        """
        Gets the first empty square in the column, if there is one.
        Pieces are added to a column from the bottom-up, so the returned square is the first empty square found when
        searching the rows in the column in ascending order.

        Args:
            column: The index of the column to search in.

        Returns:
            The first empty square in the column, or `None` if the column has no empty squares.
        """
        column_squares: list[Square] = [row[column] for row in self._current_squares]
        """A list of all the squares in the selected column."""

        # Iterate through `column_squares` and return the first empty square.
        # If there are no empty squares, return `None`.
        return next((square for square in column_squares if square.piece_id == square.NO_PIECE), None)

    def is_valid_move(self, selected_square: Square) -> bool:
        """
        Checks if a move is valid.
        A move is valid if the column the selected square is in has empty squares, and the game is not over.

        The piece will not necessarily be placed where `selected_square` is -- it will be placed on
        the first empty square of its column. Hence, `selected_square` can be valid even if there is already a piece in it.

        Args:
            selected_square: The square selected for the move. The square is not necessarily where the piece will be placed.

        Returns:
            `True` if the move is valid, `False` otherwise.
        """
        # Checks if there is an empty square in the selected square's column
        column_has_empty_square: bool = self.get_first_empty_square_in_column(selected_square.column) is not None
        game_is_not_over: bool = not self._has_winner  # The game is not over if there is no winner

        return column_has_empty_square and game_is_not_over

    def handle_move(self, selected_square: Square):
        """
        Places the player's piece in the first empty square in the column, and checks if there is a win, i.e. a four-in-a-row.
        The move should be valid, and should be checked beforehand.

        Args:
            selected_square: The square selected for the move. The square is not necessarily where the piece will be placed.
        """
        # TODO: Place piece in first empty square using get_first_empty_square_in_column
        #   maybe check for None?
        # check row, column, and diagonals of the placed piece for a four-in-a-row
        #   may need to create private helper functions for these
        #   watch out for out of bounds errors
