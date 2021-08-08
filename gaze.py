# M.T. Fabellar, H. Escasinas, T.J. Damiray
# CPE 2 - 2

# This GUI program is an inventory desktop application for Book Shop.

from tkinter import *
from login import StartPage
from user import User
from admin import Admin
import sqlite3

root = Tk()
root.state('zoomed')
root.iconbitmap('logo.ico')

data_con = sqlite3.connect('userdb.db')

users = data_con.cursor()

users.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    PRIMARY KEY(user_id AUTOINCREMENT))
    """)

data_con.commit()   

books_con = sqlite3.connect('booksdb.db')

books = books_con.cursor()

books.execute("""CREATE TABLE IF NOT EXISTS bookinfos (
    book_id INTEGER,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    publisher VARCHAR(50),
    isbn INT UNSIGNED,
    quantity INT UNSIGNED NOT NULL, 
    value INT UNSIGNED NOT NULL,
    profit INT UNSIGNED NOT NULL, 
    status TEXT NOT NULL, 
    investment INT UNSIGNED, 
    expected_profit INT UNSIGNED, 
    PRIMARY KEY(book_id AUTOINCREMENT))
    """)

books_con.commit()


class MainApp:
    def __init__(self, main):
        self.window = main
        self.window.title('GAZE')
        self.window.minsize(800, 800)

        container = Frame(self.window)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, User, Admin):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == '__main__':
    app = MainApp(root)
    root.mainloop()
