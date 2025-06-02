"""Handles the win detection for a placed piece."""

import logic as Logic

def detect_win_in_row(logic: "Logic.Logic", row: int) -> list[tuple[int, int]] | None:
    """Detects if there is a win in a row.
    
    Parameters:
        logic: The current game's logic.
        row: The index of the row being checked.
    
    Returns:
        If there is a win, returns a list of the winning coordinates, e.g. [(0, 2), (0, 3), (0, 4), (0, 5)].
          Only the first 4 winning coordinates are returned.
        If there is no win, returns `None`.
    """
    row_squares: list[Logic.Square] = logic.current_squares[row]
    """A list of all the squares in the row."""
    row_as_string: str = "".join(str(square.player_id) for square in row_squares)
    """The row represented as a string, where each character represents the piece in the square, e.g. "0211112"."""
    win_start_column: int = row_as_string.find(logic.current_player.winning_combination)
    """The column the winning combination starts on, or -1 if there is no win."""

    if win_start_column >= 0: return [(row, win_start_column + i) for i in range(Logic.COMBINATION_LENGTH)]  # Win found
    else: return None  # No win found

def detect_win_in_column(logic: "Logic.Logic", column: int) -> list[tuple[int, int]] | None:
    """Detects if there is a win in a column.

    Parameters:
        logic: The current game's logic.
        column: The index of the column being checked.

    Returns:
        If there is a win, returns a list of the winning coordinates, e.g. [(0, 2), (1, 2), (2, 2), (3, 2)].
          Only the first 4 winning coordinates are returned.
        If there is no win, returns `None`.
    """
    column_squares: list[Logic.Square] = [row[column] for row in logic.current_squares]
    """A list of all the squares in the column."""
    column_as_string: str = "".join(str(square.player_id) for square in column_squares)
    """The column represented as a string, where each character represents the piece in the square, e.g. "2111100"."""
    win_start_row: int = column_as_string.find(logic.current_player.winning_combination)
    """The row the winning combination starts on, or -1 if there is no win."""

    if win_start_row >= 0: return [(win_start_row + i, column) for i in range(Logic.COMBINATION_LENGTH)]  # Win found
    else: return None  # No win found