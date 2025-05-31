"""
Contains tests for the application using pytest.
The tests are ran from the command line with the command: pytest
"""

from logic import BOARD_ROWS, Logic, Square
import pytest


@pytest.fixture(scope="function")
def logic() -> Logic:
    """Creates a `Logic` instance for testing. A new instance is created for each test function."""
    return Logic()


def test_get_first_empty_square_in_column(logic: Logic) -> None:
    """Tests `Logic.get_first_empty_square_in_column()` by checking that the coordinates of the first empty square in the column
    correctly updates as pieces are placed in the column. Then, tests it with a full column.
    """
    column: int = 3
    """The index of the column to test."""

    # Checks that the coordinates of the first empty square in the column correctly updates as pieces are placed in the column.
    # This loop continues until the column is full.
    for row in range(BOARD_ROWS):
        assert logic.get_first_empty_square_in_column(column) == Square(row, column, Square.NO_ID), \
               f"The first empty square should be: Square({row}, {column}, {Square.NO_ID})."
        logic.handle_move(column)

    # Checks that the column is full, since there should be no empty squares in it.
    assert logic.get_first_empty_square_in_column(column) is None, "A full column should not have empty squares."


def test_check_for_win_in_row(logic: Logic) -> None:
    """Tests `Logic._check_for_win_in_row` by simulating a win via four-in-a-row in a row."""

    # Simulates a Player 1 win by making a row with [2211112].
    logic.handle_move(3)  # Player 1's move: [0001000]
    logic.handle_move(0)  # Player 2's move: [2001000]
    logic.handle_move(2)  # Player 1's move: [2011000]
    logic.handle_move(1)  # Player 2's move: [2211000]
    logic.handle_move(5)  # Player 1's move: [2211010]
    logic.handle_move(6)  # Player 2's move: [2211012]
    logic.handle_move(4)  # Player 1's move: [2211112]

    # Checks that the game is won.
    assert logic._has_winner == True, "The game did not have a row winner."


def test_check_for_win_in_column(logic: Logic) -> None:
    """Tests `Logic._check_for_win_in_column` by simulating a win via four-in-a-row in a column."""

    # Simulates a Player 1 win by making a column with [1111000].
    logic.handle_move(2)  # Player 1's move: [1000000]
    logic.handle_move(1)  # Player 2's move: [1000000]
    logic.handle_move(2)  # Player 1's move: [1100000]
    logic.handle_move(1)  # Player 2's move: [1100000]
    logic.handle_move(2)  # Player 1's move: [1110000]
    logic.handle_move(1)  # Player 2's move: [1110000]
    logic.handle_move(2)  # Player 1's move: [1111000]

    # Checks that the game is won.
    assert logic._has_winner == True, "The game did not have a column winner."