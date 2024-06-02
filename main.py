from tkinter import Tk
import screens.login_screen as login_screen
import screens.registration_screen as registration_screen
import screens.home_screen as home_screen
import boards.board as board
import boards.bot_board as bot_board
import boards.online_board as online_board
from contants.app_const import WINDOW_SIZE


def main():
    window = Tk()
    window.title("Login & Registration System")
    window.geometry(WINDOW_SIZE)

    def show_login():
        login_screen.show_login_form(window, show_registration, show_home)

    def show_registration():
        registration_screen.show_registration_form(window, show_login)

    def show_home(username):
        for widget in window.winfo_children():
            widget.destroy()
        home_screen.show_home_screen(
            window, username, start_game, start_bot_game, start_online_game
        )

    def start_game(size, username):
        for widget in window.winfo_children():
            widget.destroy()
        board.create_game_board(size, window, username, show_home)

    def start_bot_game(size, username):
        for widget in window.winfo_children():
            widget.destroy()
        bot_board.create_game_board(size, window, username, show_home)

    def start_online_game(isHost, size, ip, port, username):
        for widget in window.winfo_children():
            widget.destroy()
        online_board.create_game_board(
            size, window, isHost, ip, port, username, show_home
        )

    show_login()
    window.mainloop()


if __name__ == "__main__":
    main()
