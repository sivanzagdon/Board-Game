import random
from tkinter import Canvas, Button, Label, Frame, messagebox
import db.database as database


class GameBoard(Frame):
    def __init__(
        self,
        master,
        cols=7,
        rows=6,
        username="Player",
        back_to_home_callback=None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.cols = cols
        self.rows = rows
        self.username = username
        self.pack(fill="both", expand=True)
        self.configure(bg="blue")

        self.player_color = "yellow"
        self.bot_color = "red"
        self.back_to_home_callback = back_to_home_callback

        self.current_player = self.player_color  # Start with the player

        self.turn_label = Label(
            self,
            text=self.username + " Turn",
            font=("Arial", 16),
            bg="blue",
            fg="white",
        )
        self.turn_label.pack(side="top", fill="x", pady=10)

        self.canvas = Canvas(self, bg="blue")
        self.canvas.pack(fill="both", expand=True)

        self.exit_button = Button(self, text="Exit Game", command=self.master.quit)
        self.exit_button.pack(side="bottom", pady=10)

        self.pieces = [[None for _ in range(cols)] for _ in range(rows)]
        self.initialize_board()
        self.bind_events()

    def initialize_board(self):
        self.update_idletasks()  # Makes sure the canvas is ready before drawing
        self.redraw_board()

    def redraw_board(self):
        self.canvas.delete("all")
        cell_width = self.canvas.winfo_width() / self.cols
        cell_height = self.canvas.winfo_height() / self.rows
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * cell_width + cell_width * 0.1
                y1 = row * cell_height + cell_height * 0.1
                x2 = x1 + cell_width * 0.8
                y2 = y1 + cell_height * 0.8
                self.canvas.create_oval(x1, y1, x2, y2, fill="white", tags="slot")

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.process_turn)
        self.master.bind("<Configure>", self.on_resize)  # Handles dynamic resizing

    def unbind_events(self):
        self.canvas.unbind("<Button-1>")
        self.master.unbind("<Configure>")

    def on_resize(self, event):
        self.redraw_board()

    def process_turn(self, event):
        if self.current_player != self.player_color:
            return

        col = int(event.x / (self.canvas.winfo_width() / self.cols))
        if self.make_move(col, self.player_color):
            if self.current_player != self.player_color:
                self.after(500, self.bot_move)

    def make_move(self, col, color):
        for row in reversed(range(self.rows)):
            if self.pieces[row][col] is None:
                self.pieces[row][col] = color
                self.draw_piece(row, col, color)
                if self.check_winner(row, col):
                    winner = self.username if color == self.player_color else "Bot"
                    rank = self.add_rank(winner)
                    messagebox.showinfo(
                        "Game Over", f"{winner} wins! You Got {rank} Points!"
                    )
                    self.unbind_events()
                    self.back_to_home_callback(self.username)
                    return False
                self.switch_player()
                return True
        return False

    def add_rank(self, winner):
        rank = 50 if self.username == winner else 10
        database.update_user_rank(self.username, rank)
        return rank

    def bot_move(self):
        move = self.evaluate_best_move(self.bot_color)
        if move is not None:
            self.make_move(move, self.bot_color)

    def evaluate_best_move(self, color):
        opponent = "yellow" if color == "red" else "red"
        center_column = self.cols // 2
        best_score = -float("inf")
        best_col = random.choice(
            [c for c in range(self.cols) if self.pieces[0][c] is None]
        )  # fallback to random

        # Score each column
        for col in range(self.cols):
            if self.pieces[0][col] is not None:
                continue  # skip full columns

            row = self.get_next_open_row(col)
            if row is None:
                continue

            # Temporarily make the move
            self.pieces[row][col] = color

            # Check if this move wins the game
            if self.check_winner(row, col):
                self.pieces[row][col] = None  # Undo the move
                return col  # Return immediately if winning move found

            # Evaluate blocking the opponent
            self.pieces[row][col] = opponent
            if self.check_winner(row, col):
                score = 1000  # High score for blocking opponent
            else:
                score = 0

            # Prefer center columns
            score += (self.cols // 2 - abs(col - center_column)) * 10

            # Undo the move
            self.pieces[row][col] = None

            # Choose the best column based on score
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    def get_next_open_row(self, col):
        """Helper function to find the next open row in the given column"""
        for r in range(self.rows - 1, -1, -1):
            if self.pieces[r][col] is None:
                return r
        return None

    def draw_piece(self, row, col, color):
        cell_width = self.canvas.winfo_width() / self.cols
        cell_height = self.canvas.winfo_height() / self.rows
        x1 = col * cell_width + cell_width * 0.2
        y1 = row * cell_height + cell_height * 0.2
        x2 = x1 + cell_width * 0.6
        y2 = y1 + cell_height * 0.6
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, tags="piece")

    def switch_player(self):
        self.current_player = (
            self.bot_color
            if self.current_player == self.player_color
            else self.player_color
        )
        current_turn = (
            self.username if self.current_player == self.player_color else "Bot"
        )
        self.turn_label.config(text=f"{current_turn}'s Turn")

    def is_player_turn(self):
        return self.current_player == self.player_color

    def check_winner(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for n in range(1, 4):
                r = row + dr * n
                c = col + dc * n
                if (
                    r < 0
                    or r >= self.rows
                    or c < 0
                    or c >= self.cols
                    or self.pieces[r][c] != self.current_player
                ):
                    break
                count += 1
            for n in range(1, 4):
                r = row - dr * n
                c = col - dc * n
                if (
                    r < 0
                    or r >= self.rows
                    or c < 0
                    or c >= self.cols
                    or self.pieces[r][c] != self.current_player
                ):
                    break
                count += 1
            if count >= 4:
                return True
        return False


def create_game_board(size, parent_window, username, back_to_home_callback):
    for widget in parent_window.winfo_children():
        widget.destroy()
    game_board = GameBoard(
        parent_window,
        cols=size,
        rows=6,
        bg="blue",
        username=username,
        back_to_home_callback=back_to_home_callback,
    )
    game_board.pack(fill="both", expand=True)
