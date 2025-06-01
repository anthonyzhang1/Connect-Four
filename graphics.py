"""Handles the game's graphics using tkinter."""

from logic import BOARD_COLUMNS, BOARD_ROWS, Logic, Square
from tkinter import font
import numpy
import tkinter

class Graphics(tkinter.Tk):
    """The game's graphics, including its window, label, and board."""
    def __init__(self, logic: Logic) -> None:
        """Initializes the game's graphics.
        
        Parameters:
            logic: The game's logic.
        """
        super().__init__()  # Inherit from tkinter

        self._buttons: dict[tkinter.Button] = {}
        """The buttons making up the board."""
        self._logic: Logic = logic
        """The game's logic."""

        self.title("Connect Four")  # The window's title
        self._create_menu()
        self._create_label()
        self._create_board()

    def _create_menu(self) -> None:
        """Creates a menu with options to start a new game, exit the game, etc."""
        menu_bar = tkinter.Menu(master=self)
        self.config(menu=menu_bar)  # Sets `menu_bar` as the main menu

        file_menu = tkinter.Menu(master=menu_bar, tearoff="off")  # The "File" option in the menu
        file_menu.add_command(label="New Game", command=self.reset_board)  # Adds an option to start a new game
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=quit)  # Adds an option to quit the game

        menu_bar.add_cascade(label="File", menu=file_menu)  # Adds the "File" option to the menu bar

    def _create_label(self) -> None:
        """Creates the label shown above the board for displaying messages."""
        display_frame = tkinter.Frame(master=self)
        display_frame.pack(fill=tkinter.X)

        # The label
        self.display = tkinter.Label(
            master=display_frame,
            text=f"Player {self._logic.current_player.id} ({self._logic.current_player.colour}), make the first move!",
            fg=self._logic.current_player.colour,
            font=font.Font(family="Arial", size=20, weight="bold")
        )

        self.display.pack()

    def _create_board(self) -> None:
        """Creates the board with a grid of buttons."""
        board_frame = tkinter.Frame(master=self)
        board_frame.pack()

        for row, column in numpy.ndindex(BOARD_ROWS, BOARD_COLUMNS):
            # Creates empty buttons
            button = tkinter.Button(
                master=board_frame,
                text="",
                font=font.Font(size=60),  # Affects the size of the button
                width=3  # Affects the button's proportions
            )

            self._buttons[button] = (row, column)  # Assigns the button's coordinates
            button.bind("<ButtonPress-1>", self.play)  # Clicking the button calls play()
            button.grid(row=row, column=column)  # Places the button into the board's grid

    def _get_actual_button(self, clicked_button: tkinter.Button) -> tkinter.Button | None:
        """Gets the actual button the piece was placed in, which is not necessarily the clicked one.
        The piece is placed in the first empty button of a column.

        Parameters:
            clicked_button: The clicked button.

        Returns:
            The actual button the piece was placed in if the move was valid, and `None` otherwise.
        """
        actual_square: Square | None = self._logic.get_first_empty_square_in_column(self._buttons[clicked_button][1])
        """The piece's actual square, if the move was valid. `None` otherwise."""

        if actual_square is None: return None  # If the move was invalid

        actual_row: int = BOARD_ROWS - actual_square.row - 1
        """The piece's actual row on the grid, translated from the logic's row index."""

        # Returns the actual button matching the piece's coordinates
        return [button for button, coordinates in self._buttons.items() if coordinates == (actual_row, actual_square.column)][0]

    def _display_piece(self, button: tkinter.Button) -> None:
        """Displays the current player's piece on a button."""
        button.config(
            text="⬤",  # The displayed piece
            fg=self._logic.current_player.colour  # The piece's colour
        )

    def _highlight_winning_squares(self) -> None:
        """Highlights the buttons containing the winning combination."""
        button: tkinter.Button
        winning_coordinates: list[tuple[int, int]] = [(BOARD_ROWS - coordinates[0] - 1, coordinates[1])
                                                      for coordinates in self._logic.winning_coordinates]
        """The grid's winning coordinates, translated from the logic's winning coordinates."""

        # Finds the buttons with the winning coordinates and highlights them with the winner's colour
        for button, coordinates in self._buttons.items():
            if coordinates in winning_coordinates:
                button.config(
                    default="active",  # Highlights the button
                    highlightcolor=self._logic.current_player.colour,
                    highlightthickness=3
                )

    def _update_label(self, message: str, colour: str) -> None:
        """Updates the label with the given message and colour."""
        self.display.config(text=message, fg=colour)

    def play(self, event: tkinter.Event) -> None:
        """Handles a player's move.
        
        Parameters:
            event: A button press.
        """
        clicked_button: tkinter.Button = event.widget
        """The button clicked by the user."""
        clicked_column = self._buttons[clicked_button][1]
        """The column of the clicked button."""

        if not self._logic.is_valid_move(clicked_column): return  # Discard invalid moves
        
        actual_button: tkinter.Button = self._get_actual_button(clicked_button)
        """The actual button with the placed piece."""
        
        self._display_piece(actual_button)  # Display the piece placed in the button
        self._logic.handle_move(clicked_column)  # Handles the move's logic

        # If the game is tied, switch who goes first in the next game
        if self._logic.is_tied():
            self._update_label("The game has ended in a tie.", "black")
            self._logic.switch_to_next_player()
        
        # If the game is won, highlight the winning squares and switch who goes first in the next game
        elif self._logic._has_winner:
            self._highlight_winning_squares()
            message = f"Player {self._logic.current_player.id} ({self._logic.current_player.colour}) wins!"
            self._update_label(message, self._logic.current_player.colour)
            self._logic.switch_to_next_player()

        # If the game is ongoing, just update the label
        else:
            message = f"Player {self._logic.current_player.id} ({self._logic.current_player.colour})'s turn."
            self._update_label(message, self._logic.current_player.colour)

    def reset_board(self) -> None:
        """Resets the game's label and board to a new game state."""
        self._logic.reset_game()  # Resets the game's logic
        message = f"Player {self._logic.current_player.id} ({self._logic.current_player.colour}), make the first move!"
        self._update_label(message, self._logic.current_player.colour)

        # Resets the board's buttons to their initial state
        for button in self._buttons.keys():
            button.config(
                default="normal",  # Undoes a button's highlighting from a won game
                highlightthickness=0,  # Undoes a button's highlighting from a won game
                text=""
            )

def main() -> None:
    """Launches the game."""
    Graphics(Logic()).mainloop()

if __name__ == "__main__": main()