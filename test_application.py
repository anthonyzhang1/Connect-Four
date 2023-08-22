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
    """Tests `Logic.get_first_empty_square_in_column()` by checking that
    the coordinates of the first empty square in the column correctly updates as pieces are placed in the column.
    Then, tests `Logic.get_first_empty_square_in_column()` with a full column.
    """
    column: int = 3
    """The index of the column to test."""

    # Checks that the coordinates of the first empty square in the column correctly updates as pieces are placed in the column.
    # This loop continues until the column is full.
    for row in range(BOARD_ROWS):
        assert logic.get_first_empty_square_in_column(column) == Square(row, column, Square.NO_ID), \
               f"The first empty square should be: Square({row}, {column}, {Square.NO_ID})."
        logic.handle_move(column)
        logic.switch_to_next_player()  # Alternate players to avoid four-in-a-row in the column

    # Checks that the column is full, since there should be no empty squares in it.
    assert logic.get_first_empty_square_in_column(column) is None, "A full column should have no empty squares."
