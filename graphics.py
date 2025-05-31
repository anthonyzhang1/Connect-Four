"""Handles the game's graphics using tkinter."""

from logic import BOARD_ROWS, BOARD_COLUMNS, Logic
from tkinter import font
import numpy
import tkinter


class Graphics(tkinter.Tk):
    """The game's graphics, including its window, label, and board."""

    _BUTTON_FOREGROUND_COLOUR = "black"
    """The foreground colour for the buttons used for the board."""
    _BUTTON_HIGHLIGHT_BACKGROUND_COLOUR = "lightblue"
    """The highlight background colour for the buttons used for the board."""

    def __init__(self, logic: Logic) -> None:
        """Initializes the game's graphics.

        Args:
            logic: The logic for the game.
        """
        super().__init__()  # Inherit from tkinter

        self._squares: dict[tkinter.Button] = {}
        """The squares in the board, made up of tkinter buttons."""
        self._logic: Logic = logic
        """The game's logic."""

        self.title("Connect Four")  # The window's title
        self._create_label()
        self._create_board()

    def _create_label(self) -> None:
        """Creates the label shown above the board."""
        display_frame = tkinter.Frame(master=self)
        display_frame.pack(fill=tkinter.X)

        # The label
        self.display = tkinter.Label(
            master=display_frame,
            text=f"Player {self._logic.current_player.id} ({self._logic.current_player.colour}), make the first move!",
            font=font.Font(family="Arial", size=20, weight="bold"),
        )

        self.display.pack()

    def _create_board(self) -> None:
        """Creates the board using a grid of buttons."""
        board_frame = tkinter.Frame(master=self)
        board_frame.pack()

        # Creates an empty button for every square in the board
        for row, column in numpy.ndindex(BOARD_ROWS, BOARD_COLUMNS):
            button = tkinter.Button(
                master=board_frame,
                text="",
                font=font.Font(size=30),  # Determines the size of the squares
                fg=self._BUTTON_FOREGROUND_COLOUR,
                highlightbackground=self._BUTTON_HIGHLIGHT_BACKGROUND_COLOUR,
                width=4,
                height=2,
            )

            self._squares[button] = (row, column)  # The buttons are now the squares in the board

            # Creates the board using a grid of buttons
            button.grid(
                column=column,
                row=row,
                padx=1,  # Padding between columns
                pady=1,  # Padding between rows
            )

    # TODO: Update the game's graphics after finishing the game logic.


def main() -> None:
    """Launches the game."""
    Graphics(Logic()).mainloop()


if __name__ == "__main__":
    main()