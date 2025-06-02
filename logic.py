"""Handles the game's logic."""

from itertools import cycle
from win_detection import detect_win_in_ascending_diagonal, detect_win_in_descending_diagonal, detect_win_in_column, detect_win_in_row

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

        Parameters:
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

        Parameters:
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

        Parameters:
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
        self.current_squares: list[list[Square]] = []
        """A list with all of the squares in the board, in the form [row][column]."""
        self.has_winner: bool = False
        """Used to determine if the game has a winner."""
        self.winning_coordinates: list[tuple[int, int]] = []
        """The coordinates of the squares which won the game, e.g. [(0, 2), (0, 3), ...]"""
        self.current_player: Player = next(self._players)
        """The player whose turn it is."""

        self._initialize_board()

    def _initialize_board(self) -> None:
        """Initialize all of the squares in the board, in the form [row][column]."""
        self.current_squares = [[Square(row, column) for column in range(BOARD_COLUMNS)] for row in range(BOARD_ROWS)]

    def reset_game(self) -> None:
        """Resets the game's logic to a new game state."""
        self._initialize_board()
        # Resets variables related to the game's winner
        self.has_winner = False
        self.winning_coordinates = []

    def switch_to_next_player(self) -> None:
        """Switches the current player to the next player."""
        self.current_player = next(self._players)

    def get_first_empty_square_in_column(self, column: int) -> Square | None:
        """Gets the first empty square in the given column, if there is one.

        Parameters:
            column: The index of the column to search in.

        Returns:
            The first empty square in the column, or `None` if the column has no empty squares.
        """
        column_squares: list[Square] = [row[column] for row in self.current_squares]
        """A list of all the squares in the given column."""

        # Iterate through `column_squares` and return the first empty square.
        # If there are no empty squares, return `None`.
        return next((square for square in column_squares if square.player_id == square.NO_ID), None)

    def is_valid_move(self, selected_column: int) -> bool:
        """Checks if a move is valid.
        A move is valid if the selected column has an empty square, and the game is ongoing (i.e. not over).

        Parameters:
            selected_column: The column selected for the move.

        Returns:
            `True` if the move is valid, `False` otherwise.
        """
        # Checks if there is an empty square in the selected column
        column_has_empty_square: bool = self.get_first_empty_square_in_column(selected_column) is not None
        game_is_ongoing: bool = not self.has_winner  # The game is ongoing if there is no winner

        return column_has_empty_square and game_is_ongoing
    
    def is_tied(self) -> bool:
        """Determines if the game is tied, i.e. if there is no winner and the entire top row is full.

        Returns:
            `True` if the game is tied, and `False` otherwise.
        """
        no_winner = not self.has_winner
        
        top_row_list: list[Square] = self.current_squares[BOARD_ROWS - 1]
        """A list of squares in the top row."""
        top_row_string: str = "".join(str(square.player_id) for square in top_row_list)
        """The pieces in the squares on the top row, e.g. "1222111"."""
        top_row_is_full: bool = top_row_string.find(str(Square.NO_ID)) == -1
        """Whether the top row is full, i.e. it contains no empty squares (represented by `NO_ID`)."""

        return no_winner and top_row_is_full

    def handle_move(self, column: int) -> None:
        """Places the current player's piece in the first empty square in the column, and checks if there is a win.
        Invalid moves are discarded.

        If there is a win, the winner and the winning coordinates are saved.
          Only the first 4 coordinates of the first four-in-a-row found are saved.
        If there is no win, it becomes the next player's turn.

        Parameters:
            column: The column to make the move in.
        """
        actual_square: Square | None = self.get_first_empty_square_in_column(column)
        """The square holding the placed piece. `None` if the move is invalid."""

        if actual_square is None: return  # Discard invalid moves

        # Places the piece in `actual_square`
        self.current_squares[actual_square.row][actual_square.column].player_id = self.current_player.id
        
        # Check for wins in `actual_square`'s row
        winning_coordinates: list[tuple[int, int]] | None = detect_win_in_row(self, actual_square.row)

        # If the game isn't won yet, check for wins in `actual_square`'s column
        if winning_coordinates is None: winning_coordinates = detect_win_in_column(self, actual_square.column)

        # If the game isn't won yet, check for wins in `actual_square`'s ascending diagonal
        if winning_coordinates is None:
            winning_coordinates = detect_win_in_ascending_diagonal(self, actual_square.row, actual_square.column)

        # If the game isn't won yet, check for wins in `actual_square`'s descending diagonal
        if winning_coordinates is None:
            winning_coordinates = detect_win_in_descending_diagonal(self, actual_square.row, actual_square.column)

        if winning_coordinates is None: self.switch_to_next_player()  # If there is no win
        else:  # If there is a win
            self.has_winner = True
            self.winning_coordinates = winning_coordinates