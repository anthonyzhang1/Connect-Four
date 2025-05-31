"""Handles the game's graphics using tkinter."""

from logic import BOARD_ROWS, BOARD_COLUMNS, Logic, Square
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

    # TODO: add menu

    def _create_label(self) -> None:
        """Creates the label shown above the board."""
        display_frame = tkinter.Frame(master=self)
        display_frame.pack(fill=tkinter.X)

        # The label
        self.display = tkinter.Label(
            master=display_frame,
            text=f"Player {self._logic.current_player.id} ({self._logic.current_player.colour}), make the first move!",
            fg=self._logic.current_player.colour,
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
                font=font.Font(size=60),  # Determines the size of the squares
                width=3
            )

            self._squares[button] = (row, column)  # The buttons are now the squares in the board
            button.bind("<ButtonPress-1>", self.play)  # Binds the click event of every button with play()

            # Creates the board using a grid of buttons
            button.grid(
                column=column,
                row=row,
                padx=1,  # Padding between columns
                pady=0,  # Padding between rows
            )

    def _get_actual_button(self, clicked_button: tkinter.Button) -> tkinter.Button:
        """Gets the button that will actually show the piece.
        The button that needs to change colour is the one with the first empty square.
        """
        square = self._logic.get_first_empty_square_in_column(self._squares[clicked_button][1])
        grid_row = BOARD_ROWS - square.row - 1
        keys = [key for key, val in self._squares.items() if val == (grid_row, square.column)]
        return keys[0]

    def _display_piece(self, clicked_button: tkinter.Button):
        """Displays the current player's piece on the clicked button.
        
        Args:
            clicked_button: The clicked button.
        """
        clicked_button.config(
            text="⬤",  # The colour of the piece
            fg=self._logic.current_player.colour
        )


    def _highlight_winning_squares(self):
        """Highlights the squares containing the winner's combination."""
        button: tkinter.Button
        actual_winning_coordinates = [(BOARD_ROWS - val[0] - 1, val[1]) for val in self._logic.winning_coordinates]
        for button, coordinates in self._squares.items():
            # Finds the winner's combination and highlights them with the winner's colour.
            if coordinates in actual_winning_coordinates:
                button.config(
                    default="active",
                    highlightcolor=self._logic.current_player.colour,
                    highlightthickness=3
                )


    def _update_label(self, message, colour):
        """Updates the label shown above the board with the given message and colour."""
        self.display.config(text=message, fg=colour)


    def play(self, event: tkinter.Event) -> None:
        """Handles a player's move.
        
        Args:
            event: A button press.
        """
        clicked_button = event.widget  # The button pressed on the board
        column = self._squares[clicked_button][1]  # The row and column of the clicked button

        # If the move is invalid, do nothing
        if not self._logic.is_valid_move(column):
            return
        
        actual_button = self._get_actual_button(clicked_button)
        # If the move is valid:
        self._display_piece(actual_button)  # Display the current player's piece on the clicked button
        self._logic.handle_move(column)  # Processes the move

        if self._logic._has_winner:  # If game is won
            self._highlight_winning_squares()  # Highlights the winning squares
            message = f"Player {self._logic.current_player.id} ({self._logic.current_player.colour}) won!"
            message_colour = self._logic.current_player.colour
            self._update_label(message, message_colour)
        else:  # If the game is not over yet
            message = f"Player {self._logic.current_player.id} ({self._logic.current_player.colour})'s turn."
            message_colour = self._logic.current_player.colour
            self._update_label(message, message_colour)

    # TODO: add reset board

def main() -> None:
    """Launches the game."""
    Graphics(Logic()).mainloop()


if __name__ == "__main__":
    main()