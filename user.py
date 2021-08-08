# User Dashboard
from tkinter import *
from tkinter import ttk
import sqlite3
from PIL import ImageTk, Image
from tkinter import messagebox

# Book's Database
book_con = sqlite3.connect('booksdb.db')

books = book_con.cursor()


class User(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.upper_image = Image.open('users.png')
        self.upper_render = ImageTk.PhotoImage(self.upper_image)
        self.upper_label = Label(self, image=self.upper_render)
        self.upper_label.image = self.upper_render
        self.upper_label.place(x=0, y=0)

        self.search_bar = Image.open('search_bar.png')
        self.search_bar_render = ImageTk.PhotoImage(self.search_bar)
        self.search_bar_label = Label(self, image=self.search_bar_render)
        self.search_bar_label.image = self.search_bar_render
        self.search_bar_label.place(x=745, y=100)

        def delete_tree():
            for i in self.tree_data.get_children():
                self.tree_data.delete(i)

        def refresh_():
            self.search.set('')
            delete_tree()
            show_info()

        # Refresh Button
        self.refresh = Image.open('refresh_2.png')
        self.refresh_render = ImageTk.PhotoImage(self.refresh)
        self.refresh_button = Button(self, image=self.refresh_render, command=refresh_, borderwidth=0)
        self.refresh_button.image = self.refresh_render
        self.refresh_button.place(x=690, y=100)

        def logout():
            answer = messagebox.askyesno("Confirmation", "Are you sure you want to logout now?")
            if answer > 0:
                controller.show_frame("StartPage")

        self.logout = Image.open('logout.png')
        self.logout_render = ImageTk.PhotoImage(self.logout)
        self.logout_button = Button(self, image=self.logout_render,
                                    borderwidth=0, bg='#87ceeb',
                                    activebackground='#87ceeb', command=logout)
        self.logout_button.image = self.logout_render
        self.logout_button.place(x=1300, y=15)

        # TreeView
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Roboto', 11), rowheight=40, fieldbackground='white')  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Roboto', 8))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        style.map("mystyle.Treeview", background=[('selected', 'lightblue')], foreground=[('selected', 'white')])
        self.tree_data = ttk.Treeview(
            self,
            columns=(1, 2, 3, 4, 5, 6, 7),
            show='headings',
            height=12,
            style="mystyle.Treeview"
        )
        self.tree_data.place(x=35, y=170)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree_data.yview)
        vsb.place(x=50+1280+2, y=170, height=200+305)

        self.tree_data.configure(yscrollcommand=vsb.set)

        self.tree_data.tag_configure("evenrow", background='white', foreground='black')
        self.tree_data.tag_configure("oddrow", background='#f1f2f3', foreground='black')

        self.tree_data.column(1, minwidth=125, width=125, anchor='center')
        self.tree_data.column(2, minwidth=300, width=300)
        self.tree_data.column(3, minwidth=250, width=250)
        self.tree_data.column(4, minwidth=200, width=200)
        self.tree_data.column(5, minwidth=125, width=125, anchor='center')
        self.tree_data.column(6, minwidth=150, width=150, anchor='center')
        self.tree_data.column(7, minwidth=150, width=150, anchor='center')

        self.tree_data.heading(1, text="Book ID")
        self.tree_data.heading(2, text="Title")
        self.tree_data.heading(3, text="Author")
        self.tree_data.heading(4, text="Publisher")
        self.tree_data.heading(5, text="ISBN")
        self.tree_data.heading(6, text="Price (₱)")
        self.tree_data.heading(7, text="Status")

        def show_info():        
            books.execute("SELECT book_id, title, author, publisher, isbn, value, status FROM bookinfos")
    
            i = 0
            for data in books:
                if i % 2 == 0:
                    self.tree_data.insert(
                        '',
                        i,
                        text='',
                        values=(
                            data[0], data[1], data[2],
                            data[3], data[4], data[5],
                            data[6],),
                        tags=('evenrow',)
                    )
                else:
                    self.tree_data.insert(
                        '',
                        i,
                        text='',
                        values=(
                            data[0], data[1], data[2],
                            data[3], data[4], data[5],
                            data[6],),
                        tags=('oddrow',)
                    )
                i += 1
        
        show_info()

        def update(rows):
            self.tree_data.delete(*self.tree_data.get_children())
            count = 0

            for i in rows:
                if count % 2 == 0:
                    self.tree_data.insert('', 'end', values=i, tags=("evenrow",))
                else:
                    self.tree_data.insert('', 'end', values=i, tags=("oddrow",))

                count += 1

            self.tree_data.tag_configure("evenrow", background='white', foreground='black')
            self.tree_data.tag_configure("oddrow", background='#f1f2f3', foreground='black')

        def search(event):
            searching = self.search.get()
            books.execute("""SELECT 
                            book_id, title, author, publisher, 
                            isbn, value, status 
                            FROM bookinfos 
                            WHERE author LIKE ? OR title LIKE ?""", (
                '%' + searching + '%',
                '%' + searching + '%')
            )

            rows = books.fetchall()
            update(rows)

        # Search Entry
        self.search = StringVar()
        self.search_entry = Entry(
            self,
            textvariable=self.search,
            width=57,
            font=('Imfortee', 12),
            borderwidth=0,
            selectbackground='skyblue'
        )
        self.search_entry.place(x=770, y=113)
        self.search_entry.bind("<KeyRelease>", search)

        # Products Label
        self.books = Label(self, text="List of Books", font=("Comfortaa", 23, 'bold'), foreground='#87ceeb')
        self.books.place(x=30, y=95)
