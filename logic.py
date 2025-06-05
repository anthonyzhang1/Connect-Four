"""Handles the game's logic."""

from itertools import cycle
from win_detection import detect_win_in_ascending_diagonal, detect_win_in_descending_diagonal, detect_win_in_column, detect_win_in_row

BOARD_ROWS = 6
"""The number of rows in the board."""
BOARD_COLUMNS = 7
"""The number of columns in the board."""
COMBINATION_LENGTH = 4
"""The number of a player's pieces in a row required to win."""

class Player:
    """A player.

    Attributes:
        id (int): The player's ID.
        colour (str): The colour of the player's pieces.
        winning_combination (str): The player's ID repeated `COMBINATION_LENGTH` times. Used to determine if the player won.
    """
    def __init__(self, id: int, colour: str) -> None:
        """Initializes the player.

        Parameters:
            id: The player's ID. Must be between 1 and 9, inclusive.
            colour: The colour of the player's pieces.
        """
        if id < 1 or id > 9: raise ValueError("`id` must be between 1 and 9, inclusive.")  # Invalid ID provided

        self.id: int = id
        """The player's ID. Between 1 and 9, inclusive."""
        self.colour: str = colour
        """The colour of the player's pieces."""
        self.winning_combination: str = str(id) * COMBINATION_LENGTH
        """The player's ID repeated COMBINATION_LENGTH times, e.g. "1111"."""

class Square:
    """A square in the board and the piece in it.

    Attributes:
        NO_ID (int): Indicates the square has no piece in it.
        row (int): The row of the square in the board.
        column (int): The column of the square in the board.
        player_id (int): The ID of the player whose piece is in the square.
    """
    NO_ID: int = 0
    """Used for `player_id` if the square has no piece in it."""

    def __init__(self, row: int, column: int, player_id: int = NO_ID) -> None:
        """Initializes the square.

        Parameters:
            row: The row the square is on.
            column: The column the square is on.
            player_id: The ID of the player whose piece is in the square. Leave blank to initialize an empty square.
        """
        self.row: int = row
        """The row the square is on in the board."""
        self.column: int = column
        """The column the square is on in the board."""
        self.player_id: int = player_id
        """The ID of the player whose piece is in the square. `NO_ID` if the square is empty."""

    def __eq__(self, other) -> bool:
        """Defines how `==` behaves.
        `Square`s are equivalent if they have the same attribute values.

        Parameters:
            other: The other object to compare to.

        Returns:
            `True` if `other` is a `Square` with the same attribute values. `False` otherwise.
        """
        if not isinstance(other, Square): return False  # `other` is not a `Square`
        
        return (self.row, self.column, self.player_id) == (other.row, other.column, other.player_id)

PLAYERS = (
    Player(id=1, colour="blue"),
    Player(id=2, colour="red")
)
"""The players in the game."""

class Logic:
    """The game's logic.

    Attributes:
        squares (list[list[Square]]): All of the board's squares.
        game_is_won (bool): Whether the game is won.
        winning_coordinates (list[tuple[int, int]]): The coordinates of the squares which won the game.
        current_player (Player): The player whose turn it is.
    """
    def __init__(self) -> None:
        """Initializes the game's logic."""
        self._players = cycle(PLAYERS)
        """The players in the game, in a cycle."""
        self.squares: list[list[Square]] = []
        """All of the board's squares, as [row][column]."""
        self.game_is_won: bool = False
        """Whether the game is won."""
        self.winning_coordinates: list[tuple[int, int]] = []
        """The coordinates of the squares which won the game, e.g. [(0, 2), (0, 3), ...]"""
        self.current_player: Player = next(self._players)
        """The player whose turn it is. If the game is won, then this is also the winner."""

        self._initialize_board()

    def _initialize_board(self) -> None:
        """Initializes all of the board's squares."""
        self.squares = [[Square(row, column) for column in range(BOARD_COLUMNS)] for row in range(BOARD_ROWS)]

    def reset_game(self) -> None:
        """Resets the game's logic to a new game state."""
        self._initialize_board()

        # Resets variables related to the winner
        self.game_is_won = False
        self.winning_coordinates = []

    def switch_players(self) -> None:
        """Switches the current player to the next player."""
        self.current_player = next(self._players)

    def get_first_empty_square_in_column(self, column: int) -> Square | None:
        """Gets the first empty square in a column, if there is one.

        Parameters:
            column: The index of the column to search.

        Returns:
            The first empty square in the column, or `None` if the column is full.
        """
        column_squares: list[Square] = [row[column] for row in self.squares]
        """The squares in the column."""

        # Iterate though `column_squares` looking for the first empty square
        return next((square for square in column_squares if square.player_id == square.NO_ID), None)

    def is_valid_move(self, column: int) -> bool:
        """Checks if a move is valid, i.e. if the column has an empty square, and the game is ongoing (has no winner).

        Parameters:
            column: The index of the column handling the move.

        Returns:
            `True` if the move is valid. `False` otherwise.
        """
        # Check if the column has an an empty square and if the game is ongoing
        column_has_empty_square: bool = self.get_first_empty_square_in_column(column) is not None
        game_is_ongoing: bool = not self.game_is_won

        return column_has_empty_square and game_is_ongoing
    
    def game_is_tied(self) -> bool:
        """Checks if the game is tied, i.e. if there is no winner and the top row is full.

        Returns:
            `True` if the game is tied. `False` otherwise.
        """
        no_winner: bool = not self.game_is_won
        """If the game has no winner."""
        top_row_squares: list[Square] = self.squares[BOARD_ROWS - 1]
        """The squares in the top row."""
        top_row_string: str = "".join(str(square.player_id) for square in top_row_squares)
        """The pieces in the top row as a string, e.g. "1222111"."""
        top_row_is_full: bool = top_row_string.find(str(Square.NO_ID)) == -1
        """Whether the top row is full, i.e. it has no empty squares."""

        return no_winner and top_row_is_full

    def handle_move(self, column: int) -> None:
        """Places the current player's piece in the first empty square in the column, then checks for a win.
        Invalid moves are discarded.

        If there is a win, the win and its first 4 winning coordinates are saved. Otherwise, it becomes the next player's turn.

        Parameters:
            column: The index of the column handling the move.
        """
        actual_square: Square | None = self.get_first_empty_square_in_column(column)
        """The square the piece is placed in. `None` if the move is invalid."""

        if actual_square is None: return  # Discard invalid moves

        # Places the piece in `actual_square`
        self.squares[actual_square.row][actual_square.column].player_id = self.current_player.id

        # Check for wins in `actual_square`'s row, column, and ascending and descending diagonals. Only the first win found is saved.
        winning_coordinates: list[tuple[int, int]] | None = detect_win_in_row(self, actual_square.row)
        if winning_coordinates is None: winning_coordinates = detect_win_in_column(self, actual_square.column)
        if winning_coordinates is None: winning_coordinates = detect_win_in_ascending_diagonal(self, actual_square.row, actual_square.column)
        if winning_coordinates is None: winning_coordinates = detect_win_in_descending_diagonal(self, actual_square.row, actual_square.column)

        if winning_coordinates is not None:  # If there is a win
            self.game_is_won = True
            self.winning_coordinates = winning_coordinates
        else: self.switch_players()  # If there is no win