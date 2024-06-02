from tkinter import Canvas, Button, Label, Frame, messagebox


class GameBoard(Frame):
    def __init__(
        self,
        master,
        cols=6,
        rows=6,
        username="Guast",
        back_to_home_callback=None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.cols = cols
        self.rows = rows
        self.pack(fill="both", expand=True)
        self.configure(bg="blue")
        self.username = username

        self.turn_label = Label(
            self, text="Yellow's Turn", font=("Arial", 16), bg="blue", fg="white"
        )
        self.turn_label.pack(side="top", fill="x", pady=10)

        self.canvas = Canvas(self, bg="blue")
        self.canvas.pack(fill="both", expand=True)

        self.back_to_home_callback = back_to_home_callback

        self.exit_button = Button(self, text="Exit Game", command=self.master.quit)
        self.exit_button.pack(side="bottom", pady=10)

        self.pieces = [[None for _ in range(cols)] for _ in range(rows)]
        self.current_player = "yellow"
        self.initialize_board()
        self.bind_events()

    def initialize_board(self):
        self.update_idletasks()
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

        for row in range(self.rows):
            for col in range(self.cols):
                if self.pieces[row][col]:
                    self.draw_piece(row, col)

    def draw_piece(self, row, col):
        cell_width = self.canvas.winfo_width() / self.cols
        cell_height = self.canvas.winfo_height() / self.rows
        x1 = col * cell_width + cell_width * 0.2
        y1 = row * cell_height + cell_height * 0.2
        x2 = x1 + cell_width * 0.6
        y2 = y1 + cell_height * 0.6
        color = self.pieces[row][col]
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, tags="piece")

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.process_turn)
        self.master.bind("<Configure>", self.on_resize)

    def unbind_events(self):
        self.canvas.unbind("<Button-1>")
        self.master.unbind("<Configure>")

    def on_resize(self, event):
        self.redraw_board()

    def process_turn(self, event):
        col = int(event.x / (self.canvas.winfo_width() / self.cols))
        for row in reversed(range(self.rows)):
            if not self.pieces[row][col]:
                self.pieces[row][col] = self.current_player
                self.draw_piece(row, col)
                if self.check_winner(row, col):
                    messagebox.showinfo(
                        "Game Over", f"{self.current_player.capitalize()} wins!"
                    )
                    self.unbind_events()
                    self.back_to_home_callback(self.username)
                    return
                self.switch_player()
                break

    def switch_player(self):
        self.current_player = "red" if self.current_player == "yellow" else "yellow"
        self.turn_label.config(text=f"{self.current_player.capitalize()}'s Turn")

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
