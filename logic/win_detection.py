"""Handles the win detection for placed pieces."""

import logic.logic as Logic

def detect_win_in_row(logic: "Logic.Logic", row: int) -> list[tuple[int, int]] | None:
    """Detects if there is a win in the row.
    
    Parameters:
        logic: The current game's logic.
        row: The index of the row being checked.
    
    Returns:
        A list with the first 4 winning coordinates if there is a win, e.g. [(0, 0), (0, 1), (0, 2), (0, 3)].
        `None` if there is no win.
    """
    row_squares: list[Logic.Square] = logic.squares[row]
    """The squares in the row."""
    row_string: str = "".join(str(square.player_id) for square in row_squares)
    """The pieces in the row as a string, e.g. "1111220"."""
    win_start_column: int = row_string.find(logic.current_player.winning_combination)
    """The column the winning combination starts on, or -1 if there is no win."""

    if win_start_column >= 0: return [(row, win_start_column + i) for i in range(Logic.COMBINATION_LENGTH)]  # Win found
    else: return None  # No win found

def detect_win_in_column(logic: "Logic.Logic", column: int) -> list[tuple[int, int]] | None:
    """Detects if there is a win in the column.

    Parameters:
        logic: The current game's logic.
        column: The index of the column being checked.

    Returns:
        A list with the first 4 winning coordinates if there is a win, e.g. [(0, 0), (1, 0), (2, 0), (3, 0)].
        `None` if there is no win.
    """
    column_squares: list[Logic.Square] = [row[column] for row in logic.squares]
    """The squares in the column."""
    column_string: str = "".join(str(square.player_id) for square in column_squares)
    """The pieces in the column as a string, e.g. "211110"."""
    win_start_row: int = column_string.find(logic.current_player.winning_combination)
    """The row the winning combination starts on, or -1 if there is no win."""

    if win_start_row >= 0: return [(win_start_row + i, column) for i in range(Logic.COMBINATION_LENGTH)]  # Win found
    else: return None  # No win found

def detect_win_in_ascending_diagonal(logic: "Logic.Logic", row: int, column: int) -> list[tuple[int, int]] | None:
    """Detects if there is a win in the ascending diagonal.

    Parameters:
        logic: The current game's logic.
        row: The index of the row being checked.
        column: The index of the column being checked.

    Returns:
        A list with the first 4 winning coordinates if there is a win, e.g. [(0, 0), (1, 1), (2, 2), (3, 3)].
        `None` if there is no win.
    """
    # Gets the ascending diagonal's origin coordinates and assigns them to `row` and `column`
    while row and column > 0:
        row -= 1
        column -= 1

    diagonal_length: int = min(Logic.BOARD_ROWS - row, Logic.BOARD_COLUMNS - column)
    """The length of the ascending diagonal. It increases as the diagonal starts closer to the bottom and left edges of the board."""
    diagonal_squares: list[Logic.Square] = [logic.squares[row + i][column + i] for i in range(diagonal_length)]
    """The squares in the ascending diagonal."""
    diagonal_string: str = "".join(str(square.player_id) for square in diagonal_squares)
    """The pieces in the diagonal as a string, e.g. "122220"."""
    win_start_offset: int = diagonal_string.find(logic.current_player.winning_combination)
    """The offset from the diagonal's origin the winning combination starts on, or -1 if there is no win."""

    if win_start_offset >= 0:  # Win found
        return [(row + win_start_offset + i, column + win_start_offset + i) for i in range(Logic.COMBINATION_LENGTH)]
    else: return None  # No win found

def detect_win_in_descending_diagonal(logic: "Logic.Logic", row: int, column: int) -> list[tuple[int, int]] | None:
    """Detects if there is a win in the descending diagonal.

    Parameters:
        logic: The current game's logic.
        row: The index of the row being checked.
        column: The index of the column being checked.

    Returns:
        A list with the first 4 winning coordinates if there is a win, e.g. [(3, 0), (2, 1), (1, 2), (0, 3)].
        `None` if there is no win.
    """
    # Gets the descending diagonal's origin coordinates and assigns them to `row` and `column`
    while row < Logic.BOARD_ROWS - 1 and column > 0:
        row += 1
        column -= 1
    
    diagonal_length: int = min(row + 1, Logic.BOARD_COLUMNS - column)
    """The length of the descending diagonal. It increases as the diagonal starts closer to the top and left edges of the board."""
    diagonal_squares: list[Logic.Square] = [logic.squares[row - i][column + i] for i in range(diagonal_length)]
    """The squares in the descending diagonal."""
    diagonal_string: str = "".join(str(square.player_id) for square in diagonal_squares)
    """The pieces in the diagonal as a string, e.g. "022221"."""
    win_start_offset: int = diagonal_string.find(logic.current_player.winning_combination)
    """The offset from the diagonal's origin the winning combination starts on, or -1 if there is no win."""

    if win_start_offset >= 0:  # Win found
        return [(row - win_start_offset - i, column + win_start_offset + i) for i in range(Logic.COMBINATION_LENGTH)]
    else: return None  # No win found