"""Tests the game's logic using pytest."""

from logic.logic import BOARD_ROWS, Logic
import pytest

@pytest.fixture(scope="function")
def logic() -> Logic:
    """Creates a new `Logic` instance for each test function."""
    return Logic()

def test_fill_column_with_pieces(logic: Logic) -> None:
    """Fills a column with pieces, then verifies that it's full."""
    column: int = 0
    """The index of the column to test."""

    for _ in range(BOARD_ROWS): logic.handle_move(column)  # Fills the column with pieces
    assert logic.get_first_empty_square_in_column(column) is None, "The column was not full."

def test_row_win_detection(logic: Logic) -> None:
    """Simulates a game where a player wins in a row."""
    # Creates this board where Player 1 wins:
    # [2,2,2,0]
    # [1,1,1,1]
    logic.handle_move(0)  # Player 1's move in Row 0: [1,0,0,0]
    logic.handle_move(0)  # Player 2's move in Row 1: [2,0,0,0]
    logic.handle_move(1)  # Player 1's move in Row 0: [1,1,0,0]
    logic.handle_move(1)  # Player 2's move in Row 1: [2,2,0,0]
    logic.handle_move(2)  # Player 1's move in Row 0: [1,1,1,0]
    logic.handle_move(2)  # Player 2's move in Row 1: [2,2,2,0]
    logic.handle_move(3)  # Player 1's move in Row 0: [1,1,1,1]

    assert logic.game_is_won == True, "There was no win in a row."  # Verifies that the game was won

def test_column_win_detection(logic: Logic) -> None:
    """Simulates a game where a player wins in a column."""
    # Creates this board where Player 1 wins:
    # [1,0]
    # [1,2]
    # [1,2]
    # [1,2]
    logic.handle_move(0)  # Player 1's move in Row 0: [1,0]
    logic.handle_move(1)  # Player 2's move in Row 0: [1,2]
    logic.handle_move(0)  # Player 1's move in Row 1: [1,0]
    logic.handle_move(1)  # Player 2's move in Row 1: [1,2]
    logic.handle_move(0)  # Player 1's move in Row 2: [1,0]
    logic.handle_move(1)  # Player 2's move in Row 2: [1,2]
    logic.handle_move(0)  # Player 1's move in Row 3: [1,0]

    assert logic.game_is_won == True, "There was no win in a column."  # Verifies that the game was won

def test_ascending_diagonal_win_detection(logic: Logic) -> None:
    """Simulates a game where a player wins in an ascending diagonal."""
    # Creates this board where Player 2 wins:
    # [0,0,0,2]
    # [0,0,2,1]
    # [0,2,1,1]
    # [2,2,1,1]
    logic.handle_move(2)  # Player 1's move on Row 0: [0,0,1,0]
    logic.handle_move(0)  # Player 2's move on Row 0: [2,0,1,0]
    logic.handle_move(3)  # Player 1's move on Row 0: [2,0,1,1]
    logic.handle_move(1)  # Player 2's move on Row 0: [2,2,1,1]
    logic.handle_move(2)  # Player 1's move on Row 1: [0,0,1,0]
    logic.handle_move(1)  # Player 2's move on Row 1: [0,2,1,0]
    logic.handle_move(3)  # Player 1's move on Row 1: [0,2,1,1]
    logic.handle_move(2)  # Player 2's move on Row 2: [0,0,2,0]
    logic.handle_move(3)  # Player 1's move on Row 2: [0,0,2,1]
    logic.handle_move(3)  # Player 2's move on Row 3: [0,0,0,2]

    assert logic.game_is_won == True, "There was no win in an ascending diagonal."  # Verifies that the game was won

def test_descending_diagonal_win_detection(logic: Logic) -> None:
    """Simulates a game where a player wins in a descending diagonal."""
    # Creates this board where Player 2 wins:
    # [2,0,0,0]
    # [1,2,0,0]
    # [1,1,2,0]
    # [1,1,2,2]
    logic.handle_move(0)  # Player 1's move on Row 0: [1,0,0,0]
    logic.handle_move(2)  # Player 2's move on Row 0: [1,0,2,0]
    logic.handle_move(1)  # Player 1's move on Row 0: [1,1,2,0]
    logic.handle_move(3)  # Player 2's move on Row 0: [1,1,2,2]
    logic.handle_move(0)  # Player 1's move on Row 1: [1,0,0,0]
    logic.handle_move(2)  # Player 2's move on Row 1: [1,0,2,0]
    logic.handle_move(1)  # Player 1's move on Row 1: [1,1,2,0]
    logic.handle_move(1)  # Player 2's move on Row 2: [0,2,0,0]
    logic.handle_move(0)  # Player 1's move on Row 2: [1,2,0,0]
    logic.handle_move(0)  # Player 2's move on Row 3: [2,0,0,0]

    assert logic.game_is_won == True, "There was no win in a descending diagonal."  # Verifies that the game was won