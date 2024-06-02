from tkinter import *
from tkinter import messagebox, font as tkfont
import db.database as database
from contants.app_styles import setup_styles
from contants.app_const import WINDOW_SIZE


def create_styled_entry(parent, styles, show=""):
    """Creates and returns a styled Entry widget."""
    return Entry(
        parent,
        font=styles["fontInput"],
        bg=styles["entryBgColor"],
        fg=styles["entryFgColor"],
        insertbackground=styles["entryFgColor"],
        bd=styles["entryBorderWidth"],
        show=show,
        relief="flat",
        highlightthickness=1,
        highlightcolor=styles["buttonColor"],
        highlightbackground=styles["bgColor"],
    )


def show_login_form(window, switch_to_registration, switch_to_home):
    styles = setup_styles()
    clear_window(window, styles)
    window.geometry(WINDOW_SIZE)

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(4, weight=1)

    form_frame = Frame(window, bg=styles["bgColor"])
    form_frame.grid(row=1, column=1, sticky="nsew", padx=30, pady=30)
    window.grid_rowconfigure(1, weight=2)

    Label(
        form_frame,
        text="Login",
        font=styles["fontLarge"],
        bg=styles["bgColor"],
        fg=styles["fgColor"],
    ).pack(anchor="center", pady=10)
    Label(
        form_frame,
        text="Username:",
        bg=styles["bgColor"],
        fg=styles["fgColor"],
        font=styles["fontInput"],
    ).pack(anchor="w")

    username_entry = create_styled_entry(form_frame, styles)
    username_entry.pack(fill="x", pady=10)

    Label(
        form_frame,
        text="Password:",
        bg=styles["bgColor"],
        fg=styles["fgColor"],
        font=styles["fontInput"],
    ).pack(anchor="w")
    password_entry = create_styled_entry(form_frame, styles, show="*")
    password_entry.pack(fill="x", pady=10)

    Button(
        form_frame,
        text="Login",
        width=15,
        command=lambda: login(
            username_entry.get(), password_entry.get(), switch_to_home
        ),
        bg=styles["buttonColor"],
        fg=styles["buttonFgColor"],
    ).pack(pady=10)
    Button(
        form_frame,
        text="Register",
        width=15,
        command=lambda: switch_to_registration(),
        bg=styles["buttonColor"],
        fg=styles["buttonFgColor"],
    ).pack()


def login(username, password, switch_to_home):
    if database.login_user(username, password):
        switch_to_home(username)
    else:
        messagebox.showerror("Error", "Invalid username or password.")


def clear_window(window, styles):
    for widget in window.winfo_children():
        widget.destroy()
    window.configure(bg=styles["bgColor"])
