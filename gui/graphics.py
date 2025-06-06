"""Handles the game's graphics using tkinter."""

from logic.logic import BOARD_COLUMNS, BOARD_ROWS, Logic, Square
import sys
import tkinter, tkinter.font

class Graphics(tkinter.Tk):
    """The game's graphics, including its window, label, and board."""
    def __init__(self, logic: Logic) -> None:
        """Initializes the game's graphics.
        
        Parameters:
            logic: The game's logic.
        """
        super().__init__()  # Inherit from tkinter

        self._buttons: dict[tkinter.Button, tuple[int, int]] = {}
        """The buttons making up the board, in the form {Button: (row, column)}."""
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
        file_menu.add_command(label="Exit", command=sys.exit)  # Adds an option to exit the game

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
            font=tkinter.font.Font(family="Arial", size=20, weight="bold")
        )

        self.display.pack()

    def _create_board(self) -> None:
        """Creates the board with a grid of buttons."""
        board_frame = tkinter.Frame(master=self)
        board_frame.pack()

        # Creates a button for each square in the grid
        for row in range(BOARD_ROWS):
            for column in range(BOARD_COLUMNS):
                # Creates an empty button
                button = tkinter.Button(
                    master=board_frame,
                    text="",
                    font=tkinter.font.Font(size=60),  # Affects the size of the button
                    width=3  # Affects the button's proportions
                )

                self._buttons[button] = (row, column)  # Assigns the button's coordinates
                button.bind("<ButtonPress-1>", self.play)  # Left-clicking the button calls play()
                
                # Places the button into the grid going from bottom-to-top rather than top-to-bottom to match the game's internal model
                button.grid(row=BOARD_ROWS - row - 1, column=column)

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

        if actual_square is None: return None  # Invalid move

        # Returns the actual button with the placed piece's coordinates
        return [button for button, coordinates in self._buttons.items() if coordinates == (actual_square.row, actual_square.column)][0]

    def _display_piece(self, button: tkinter.Button) -> None:
        """Displays the current player's piece on a button."""
        button.config(
            text="⬤",  # The displayed piece
            fg=self._logic.current_player.colour  # The piece's colour
        )

    def _highlight_winning_squares(self) -> None:
        """Highlights the buttons containing the winning combination."""
        # Finds the buttons with the winning coordinates and highlights them with the winner's colour
        for button, coordinates in self._buttons.items():
            if coordinates in self._logic.winning_coordinates:
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
        
        self._display_piece(actual_button)  # Display the placed piece in the button
        self._logic.handle_move(clicked_column)  # Handles the move's logic

        # If the game is tied, switch who goes first in the next game
        if self._logic.game_is_tied():
            self._update_label("The game has ended in a tie.", "black")
            self._logic.switch_players()
        
        # If the game is won, highlight the winning squares and switch who goes first in the next game
        elif self._logic.game_is_won:
            self._highlight_winning_squares()
            message = f"Player {self._logic.current_player.id} ({self._logic.current_player.colour}) wins!"
            self._update_label(message, self._logic.current_player.colour)
            self._logic.switch_players()

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