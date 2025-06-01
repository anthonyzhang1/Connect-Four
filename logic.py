"""Handles the game's logic."""

from itertools import cycle
from win_detection import detect_win_in_row

BOARD_ROWS = 6
"""The number of rows in the board."""
BOARD_COLUMNS = 7
"""The number of columns in the board."""
COMBINATION_LENGTH = 4
"""The number of a player's pieces in a row required to win, e.g. 4 for Connect Four."""

class Player:
    """Represents a player and their ID and colour.

    Attributes:
        id: (int) The player's ID, from 1 to 9.
        colour: (str) The colour of the player's pieces.
        winning_combination: (str) The player's ID repeated `COMBINATION_LENGTH` times.
          Used to determine if the player has four in a row.
    """
    def __init__(self, id: int, colour: str) -> None:
        """Initializes the player and their attributes.

        Args:
            id: This player's ID. Must be between 1 and 9, inclusive.
            colour: The colour of this player's pieces.
        """
        if id < 1 or id > 9:  # If invalid `id` provided
            raise ValueError("`id` must be between 1 and 9, inclusive.")

        self.id: int = id
        """The player's ID. It can be from 1 to 9."""
        self.colour: str = colour
        """The colour of the player's pieces."""
        self.winning_combination: str = str(id) * COMBINATION_LENGTH
        """The player's ID repeated COMBINATION_LENGTH times, e.g. "1111"."""

class Square:
    """Represents a square in the board and the piece within it.

    Attributes:
        NO_ID: (int) Used to indicate that a square has no piece in it.
        row: (int) The row of the square in the board.
        column: (int) The column of the square in the board.
        player_id: (int) The id of the player who placed a piece in the square.
    """
    NO_ID: int = 0
    """Used in `player_id` to indicate that the square has no piece in it."""

    def __init__(self, row: int, column: int, player_id: int = NO_ID) -> None:
        """Initializes the square and its attributes.

        Args:
            row: The row this square is on.
            column: The column this square is on.
            player_id: The ID of the player who is placing their piece in this square.
              Leave empty to indicate an empty square.
        """
        self.row: int = row
        """The row of the square in the board."""
        self.column: int = column
        """The column of the square in the board."""
        self.player_id: int = player_id
        """The ID of the player who placed a piece in the square. The value `NO_ID` means there is no piece in the square."""

    def __eq__(self, other) -> bool:
        """Defines how the `==` operator behaves for `Square`.
        `Square` objects are equivalent if they have the same `row`, `column`, and `player_id`.

        Args:
            other: The other object to compare to.

        Returns:
            `True` if `other` is a `Square` and has the same `row`, `column`, and `player_id` as `self`.
            `False` otherwise.
        """
        if not isinstance(other, Square): return False  # `other` must be a `Square` to be equivalent
        
        return (self.row, self.column, self.player_id) == (other.row, other.column, other.player_id)

PLAYERS = (
    Player(id=1, colour="blue"),
    Player(id=2, colour="red")
)
"""The players in the game."""

class Logic:
    """The game's logic.

    Attributes:
        winning_coordinates: (list[tuple[int, int]]) Contains the coordinates of the squares which won the game.
        current_player: (Player) The player whose turn it is. If the game is won, then this is also the winner.
    """
    def __init__(self) -> None:
        """Initializes the game's logic."""
        self._players = cycle(PLAYERS)
        """The players in the game, in a cycle."""
        self._current_squares: list[list[Square]] = []
        """A list with all of the squares in the board, in the form [row][column]."""
        self._has_winner: bool = False
        """Used to determine if the game has a winner."""
        self.winning_coordinates: list[tuple[int, int]] = []
        """The coordinates of the squares which won the game, e.g. [(0, 2), (0, 3), ...]"""
        self.current_player: Player = next(self._players)
        """The player whose turn it is."""

        self._initialize_board()

    def _initialize_board(self) -> None:
        """Initialize all of the squares in the board, in the form [row][column]."""
        self._current_squares = [[Square(row, column) for column in range(BOARD_COLUMNS)] for row in range(BOARD_ROWS)]

    def reset_game(self) -> None:
        """Resets the game's logic to a new game state."""
        self._initialize_board()
        # Resets variables related to the game's winner
        self._has_winner = False
        self.winning_coordinates = []

    def switch_to_next_player(self) -> None:
        """Switches the current player to the next player."""
        self.current_player = next(self._players)

    def get_first_empty_square_in_column(self, column: int) -> Square | None:
        """Gets the first empty square in the given column, if there is one.

        Args:
            column: The index of the column to search in.

        Returns:
            The first empty square in the column, or `None` if the column has no empty squares.
        """
        column_squares: list[Square] = [row[column] for row in self._current_squares]
        """A list of all the squares in the given column."""

        # Iterate through `column_squares` and return the first empty square.
        # If there are no empty squares, return `None`.
        return next((square for square in column_squares if square.player_id == square.NO_ID), None)

    def is_valid_move(self, selected_column: int) -> bool:
        """Checks if a move is valid.
        A move is valid if the selected column has an empty square, and the game is ongoing (i.e. not over).

        Args:
            selected_column: The column selected for the move.

        Returns:
            `True` if the move is valid, `False` otherwise.
        """
        # Checks if there is an empty square in the selected column
        column_has_empty_square: bool = self.get_first_empty_square_in_column(selected_column) is not None
        game_is_ongoing: bool = not self._has_winner  # The game is ongoing if there is no winner

        return column_has_empty_square and game_is_ongoing
    
    def is_tied(self) -> bool:
        """Determines if the game is tied, i.e. if there is no winner and the entire top row is full.

        Returns:
            `True` if the game is tied, and `False` otherwise.
        """
        no_winner = not self._has_winner
        
        top_row_list: list[Square] = self._current_squares[BOARD_ROWS - 1]
        """A list of squares in the top row."""
        top_row_string: str = "".join(str(square.player_id) for square in top_row_list)
        """The pieces in the squares on the top row, e.g. "1222111"."""
        top_row_is_full: bool = top_row_string.find(str(Square.NO_ID)) == -1
        """Whether the top row is full, i.e. it contains no empty squares (represented by `NO_ID`)."""

        return no_winner and top_row_is_full

    def _check_for_win_in_column(self, column: int) -> list[tuple[int, int]] | None:
        """Checks if there is four-in-a-row in the given column.

        Args:
            column: The index of the column to check.

        Returns:
            If there is a win, returns a list of the winning coordinates, e.g. [(0, 2), (1, 2), (2, 2), (3, 2)].
              Only four coordinates are returned in case of a five-in-a-row or greater.
            If there is no win, returns `None`.
        """
        column_squares: list[Square] = [row[column] for row in self._current_squares]
        """A list of all the squares in the given column."""
        column_as_string: str = "".join(str(square.player_id) for square in column_squares)
        """The column represented as a string, where each character represents the piece in the square, e.g. "1111000"."""

        # Looks for the four-in-a-row in `column_as_string` and gets the row it starts on, or -1 if there is no four-in-a-row
        combination_start_row: int = column_as_string.find(self.current_player.winning_combination)

        if combination_start_row >= 0:  # Four-in-a-row found: return the coordinates of the winning squares
            return [(combination_start_row + i, column) for i in range(COMBINATION_LENGTH)]
        else:  # No four-in-a-row found
            return None

    def _get_ascending_diagonal_start_coordinates(self, row: int, column: int) -> tuple[int, int]:
        """Gets the starting coordinates of the ascending diagonal that intersects (row, column).

        Args:
            row: The index of the checked square's row.
            column: The index of the checked square's column.

        Returns:
            Returns the row and column of the bottom-leftmost square on the intersecting ascending diagonal, e.g. (1, 0).
        """
        while row and column > 0:  # Gets the bottom-leftmost coordinate on the ascending diagonal
            row -= 1
            column -= 1

        return (row, column)

    def _check_for_win_in_ascending_diagonal(self, row: int, column: int) -> list[tuple[int, int]] | None:
        """Checks if there is a win in the given square's ascending diagonal.

        Args:
            row: The index of the checked square's row.
            column: The index of the checked square's column.

        Returns:
            If there is a win, returns a list of the winning coordinates, e.g. [(0, 1), (1, 2), (2, 3), (3, 4)].
              Only four coordinates are returned in case of a five-in-a-row or greater.
            If there is no win, returns `None`.
        """
        diagonal_start_coordinates: tuple[int, int] = self._get_ascending_diagonal_start_coordinates(row, column)
        """The coordinates of the bottom-leftmost square on the diagonal."""
        diagonal_length: int = min(BOARD_ROWS - diagonal_start_coordinates[0], BOARD_COLUMNS - diagonal_start_coordinates[1])
        """The length of the ascending diagonal. It decreases as the diagonal starts closer to the top or right edges of the board."""
        diagonal_squares: list[Square] = []
        """A list of all the squares in the ascending diagonal."""

        for i in range(diagonal_length):  # Appends all the squares on the diagonal to `diagonal_squares`
            diagonal_squares.append(self._current_squares[diagonal_start_coordinates[0] + i][diagonal_start_coordinates[1] + i])

        diagonal_as_string: str = "".join(str(square.player_id) for square in diagonal_squares)
        """The diagonal represented as a string, where each character represents the piece in the square, e.g. "222200"."""
        combination_start_offset: int = diagonal_as_string.find(self.current_player.winning_combination)
        """Stores the index (i.e. offset) of the start of the winning combination in `diagonal_as_string`, or -1 if there is no win."""

        if combination_start_offset >= 0:  # Four-in-a-row found: returns the coordinates of the winning squares
            # The winning combination's starting row and column is found with the starting coordinates + the offset
            return [(diagonal_start_coordinates[0] + combination_start_offset + i,
                     diagonal_start_coordinates[1] + combination_start_offset + i) for i in range(COMBINATION_LENGTH)]
        else:  # No four-in-a-row found
            return None
        
    def _get_descending_diagonal_start_coordinates(self, row: int, column: int) -> tuple[int, int]:
        """Gets the starting coordinates of the descending diagonal that intersects (row, column).

        Args:
            row: The index of the checked square's row.
            column: The index of the checked square's column.

        Returns:
            Returns the row and column of the top-leftmost square on the intersecting descending diagonal, e.g. (5, 0).
        """
        while row < BOARD_ROWS - 1 and column > 0:  # Gets the top-leftmost coordinate on the descending diagonal
            row += 1
            column -= 1

        return (row, column)
        
    def _check_for_win_in_descending_diagonal(self, row: int, column: int) -> list[tuple[int, int]] | None:
        """Checks if there is a win in the given square's descending diagonal.

        Args:
            row: The index of the checked square's row.
            column: The index of the checked square's column.

        Returns:
            If there is a win, returns a list of the winning coordinates, e.g. [(3, 2), (2, 3), (1, 4), (0, 5)].
              Only four coordinates are returned in case of a five-in-a-row or greater.
            If there is no win, returns `None`.
        """
        diagonal_start_coordinates: tuple[int, int] = self._get_descending_diagonal_start_coordinates(row, column)
        """The coordinates of the top-leftmost square on the diagonal."""
        diagonal_length: int = min(diagonal_start_coordinates[0] + 1, BOARD_COLUMNS - diagonal_start_coordinates[1])
        """The length of the descending diagonal. It decreases as the diagonal starts closer to the bottom or right edges of the board."""
        diagonal_squares: list[Square] = []
        """A list of all the squares in the descending diagonal."""

        for i in range(diagonal_length):  # Appends all the squares on the diagonal to `diagonal_squares`
            diagonal_squares.append(self._current_squares[diagonal_start_coordinates[0] - i][diagonal_start_coordinates[1] + i])

        diagonal_as_string: str = "".join(str(square.player_id) for square in diagonal_squares)
        """The diagonal represented as a string, where each character represents the piece in the square, e.g. "002222"."""
        combination_start_offset: int = diagonal_as_string.find(self.current_player.winning_combination)
        """Stores the index (i.e. offset) of the start of the winning combination in `diagonal_as_string`, or -1 if there is no win."""

        if combination_start_offset >= 0:  # Four-in-a-row found: returns the coordinates of the winning squares
            # The winning combination's starting row and column is found with the starting coordinates +- the offset
            return [(diagonal_start_coordinates[0] - combination_start_offset - i,
                     diagonal_start_coordinates[1] + combination_start_offset + i) for i in range(COMBINATION_LENGTH)]
        else:  # No four-in-a-row found
            return None

    def handle_move(self, column: int) -> None:
        """Places the current player's piece in the first empty square in the column, and checks if there is a win.
        The move should be validated beforehand.

        If there is a win, the winner and the winning coordinates are saved.
          Only the first 4 coordinates of the first four-in-a-row found are saved.
        If there is no win, it becomes the next player's turn.

        Args:
            column: The column the move was played in.
        """
        actual_square: Square = self.get_first_empty_square_in_column(column)
        """The square holding the placed piece."""
        
        # Places the piece in `actual_square`
        self._current_squares[actual_square.row][actual_square.column].player_id = self.current_player.id
        
        # Detects wins in `actual_square`'s row
        winning_coordinates: list[tuple[int, int]] | None = detect_win_in_row(self, actual_square.row)

        # Detects wins in `actual_square`'s column
        if winning_coordinates is None: winning_coordinates = self._check_for_win_in_column(actual_square.column)
            
        # Detects wins in `actual_square`'s ascending diagonal
        if winning_coordinates is None:
            winning_coordinates = self._check_for_win_in_ascending_diagonal(actual_square.row, actual_square.column)

        # Detects wins in `actual_square`'s descending diagonal
        if winning_coordinates is None:
            winning_coordinates = self._check_for_win_in_descending_diagonal(actual_square.row, actual_square.column)

        if winning_coordinates is None: self.switch_to_next_player()  # If there is no win
        else:  # If there is a win
            self._has_winner = True
            self.winning_coordinates = winning_coordinates