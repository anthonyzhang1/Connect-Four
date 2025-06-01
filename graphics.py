"""Handles the game's graphics using tkinter."""

from logic import BOARD_ROWS, BOARD_COLUMNS, Logic
from tkinter import font
import numpy
import tkinter


class Graphics(tkinter.Tk):
    """The game's graphics, including its window, label, and board."""
    def __init__(self, logic: Logic) -> None:
        """Initializes the game's graphics.
        
        Args:
            logic: The game's logic.
        """
        super().__init__()  # Inherit from tkinter

        self._squares: dict[tkinter.Button] = {}
        """The squares in the board, made up of tkinter buttons."""
        self._logic: Logic = logic
        """The game's logic."""

        self.title("Connect Four")  # The window's title
        self._create_menu()
        self._create_label()
        self._create_board()

    def _create_menu(self) -> None:
        """Creates a menu with options to start a new game or exit the game."""
        menu_bar = tkinter.Menu(master=self)
        self.config(menu=menu_bar)  # Sets `menu_bar` as the main menu

        file_menu = tkinter.Menu(master=menu_bar, tearoff="off")  # The "File" option in the menu
        file_menu.add_command(label="New Game", command=self.reset_board)  # Adds an option to start a new game
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=quit)  # Adds an option to quit the game

        menu_bar.add_cascade(label="File", menu=file_menu)  # Adds the "File" option to the menu bar

    def _create_label(self) -> None:
        """Creates the label shown above the board."""
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
            button.grid(row=row, column=column)

    def _get_actual_button(self, clicked_button: tkinter.Button) -> tkinter.Button:
        """Returns the button that will actually show the piece, which is not necessarily the clicked button.
        The button that shows the piece is the one with the first empty square.
        """
        actual_square = self._logic.get_first_empty_square_in_column(self._squares[clicked_button][1])
        """The actual square that will hold the piece."""
        grid_row = BOARD_ROWS - actual_square.row - 1
        """Holds the GUI's row index translated from the logic's row index."""

        # Returns the button with the matching coordinates
        return [button for button, coordinates in self._squares.items() if coordinates == (grid_row, actual_square.column)][0]

    def _display_piece(self, button: tkinter.Button) -> None:
        """Displays the current player's piece on the provided button."""
        button.config(
            text="⬤",  # The piece to display
            fg=self._logic.current_player.colour  # The colour of the piece
        )

    def _highlight_winning_squares(self) -> None:
        """Highlights the squares containing the winner's combination."""
        button: tkinter.Button
        gui_winning_coordinates = [(BOARD_ROWS - coordinates[0] - 1, coordinates[1]) for coordinates in self._logic.winning_coordinates]
        """Holds the GUI's winning coordinates translated from the logic's winning coordinates."""

        # Finds the winner's combination and highlights them with the winner's colour
        for button, coordinates in self._squares.items():
            if coordinates in gui_winning_coordinates:
                button.config(
                    default="active",
                    highlightcolor=self._logic.current_player.colour,
                    highlightthickness=3
                )

    def _update_label(self, message, colour) -> None:
        """Updates the label shown above the board with the given message and colour."""
        self.display.config(text=message, fg=colour)

    def play(self, event: tkinter.Event) -> None:
        """Handles a player's move.
        
        Args:
            event: A button press.
        """
        clicked_button = event.widget  # The button pressed on the board
        clicked_column = self._squares[clicked_button][1]  # The column of the clicked button

        # If the move is invalid, do nothing
        if not self._logic.is_valid_move(clicked_column): return
        
        actual_button: tkinter.Button = self._get_actual_button(clicked_button)
        """The button that will display the piece."""
        
        self._display_piece(actual_button)  # Display the current player's piece on the actual button
        self._logic.handle_move(clicked_column)  # Processes the move

        # If the game is tied, update the label and swap who goes first
        if self._logic.is_tied():
            self._update_label("The game has ended in a tie.", "black")
            self._logic.switch_to_next_player()
        
        # If the game is won, highlight the winning squares, update the label, and swap who goes first
        elif self._logic._has_winner:
            self._highlight_winning_squares()
            message = f"Player {self._logic.current_player.id} ({self._logic.current_player.colour}) won!"
            self._update_label(message, self._logic.current_player.colour)
            self._logic.switch_to_next_player()

        else:  # If the game is ongoing, update the label
            message = f"Player {self._logic.current_player.id} ({self._logic.current_player.colour})'s turn."
            self._update_label(message, self._logic.current_player.colour)

    def reset_board(self):
        """Resets the game's label and board to a new game state."""
        self._logic.reset_game()
        message = f"Player {self._logic.current_player.id} ({self._logic.current_player.colour}), make the first move!"
        self._update_label(message, self._logic.current_player.colour)

        # Resets all the buttons in the board to their initial state
        for button in self._squares.keys():
            button.config(
                default="normal",  # Resets the button highlighting from a won game
                text="",
                highlightthickness=0  # Realigns the grid after the buttons are highlighted
            )


def main() -> None:
    """Launches the game."""
    Graphics(Logic()).mainloop()


if __name__ == "__main__":
    main()