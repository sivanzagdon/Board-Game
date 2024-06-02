from tkinter import *
from tkinter import messagebox, font as tkfont
import db.database as database
import sqlite3
from tkinter import Tk


def setup_styles():
    """Sets up custom styles for the application."""
    return {
        "fontLarge": tkfont.Font(family="Helvetica", size=14, weight="bold"),
        "fontInput": tkfont.Font(
            family="Helvetica", size=12
        ),  # New font for input fields
        "bgColor": "#2A2D34",
        "fgColor": "#C9D1D9",
        "buttonColor": "#4E5A65",
        "buttonFgColor": "#FFFFFF",
        "entryBgColor": "#3B4048",
        "entryFgColor": "#FFFFFF",
        "entryBorderWidth": 2,  # Border width for the entry widgets
    }
