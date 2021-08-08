# Admin Dashboard
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from PIL import ImageTk, Image
import csv
import os
from tkinter import filedialog

# Book's Database
book_con = sqlite3.connect('booksdb.db')

books = book_con.cursor()


class Admin(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.upper_image = Image.open('upper.png')
        self.upper_render = ImageTk.PhotoImage(self.upper_image)
        self.upper_label = Label(self, image=self.upper_render)
        self.upper_label.image = self.upper_render
        self.upper_label.place(x=0, y=0)

        self.search_bar = Image.open('search_bar.png')
        self.search_bar_render = ImageTk.PhotoImage(self.search_bar)
        self.search_bar_label = Label(self, image=self.search_bar_render)
        self.search_bar_label.image = self.search_bar_render
        self.search_bar_label.place(x=745, y=189)

        self.money = Image.open('money.png')
        self.money_render = ImageTk.PhotoImage(self.money)
        self.money_label = Label(self, image=self.money_render)
        self.money_label.image = self.money_render
        self.money_label.place(x=20, y=90)

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

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Roboto', 8), rowheight=40, fieldbackground='white')  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Roboto', 8))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
        style.map("mystyle.Treeview", background=[('selected', 'lightblue')], foreground=[('selected', 'white')])
        self.tree_data = ttk.Treeview(
            self,
            columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
            show='headings',
            height=10,
            style="mystyle.Treeview"
        )
        self.tree_data.place(x=35, y=250)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree_data.yview)
        vsb.place(x=50+1275+2, y=250, height=200+225)

        self.tree_data.configure(yscrollcommand=vsb.set)

        self.tree_data.tag_configure("evenrow", background='white', foreground='black')
        self.tree_data.tag_configure("oddrow", background='#f1f2f3', foreground='black')

        self.tree_data.column(1, minwidth=50, width=50, anchor='center')
        self.tree_data.column(2, minwidth=225, width=225)
        self.tree_data.column(3, minwidth=150, width=150)
        self.tree_data.column(4, minwidth=150, width=150)
        self.tree_data.column(5, minwidth=125, width=125, anchor='center')
        self.tree_data.column(6, minwidth=75, width=75, anchor='center')
        self.tree_data.column(7, minwidth=125, width=125, anchor='center')
        self.tree_data.column(8, minwidth=100, width=100, anchor='center')
        self.tree_data.column(9, minwidth=100, width=100, anchor='center')
        self.tree_data.column(10, minwidth=100, width=100, anchor='center')
        self.tree_data.column(11, minwidth=100, width=100, anchor='center')

        self.tree_data.heading(1, text="Book ID")
        self.tree_data.heading(2, text="Title")
        self.tree_data.heading(3, text="Author")
        self.tree_data.heading(4, text="Publisher")
        self.tree_data.heading(5, text="ISBN")
        self.tree_data.heading(6, text="Stock")
        self.tree_data.heading(7, text="Value per Item (₱)")
        self.tree_data.heading(8, text="Profit (%)")
        self.tree_data.heading(9, text="Status")
        self.tree_data.heading(10, text="Investment (₱)")
        self.tree_data.heading(11, text="Est'd Profit (₱)")

        self.investment_label = Label(self, text='₱ 0.00',
                                      background='skyblue',
                                      foreground='white', font=("Sans", 10, 'bold'))
        self.investment_label.place(x=50, y=125)

        def total_investment():
            if len(self.tree_data.get_children()) < 1:
                self.investment_label.config(text="₱ 0.00")
            else:
                books.execute("SELECT sum(investment) FROM bookinfos")
                investment = sum(res[0] for res in books.fetchall())
                self.investment_label.config(text="₱{:,.2f}".format(investment))

        self.return_label = Label(self, text="₱ 0.00",
                                  background='skyblue',
                                  foreground='white', font=("Sans", 10, 'bold'))

        self.return_label.place(x=260, y=125)

        def total_return():
            if len(self.tree_data.get_children()) < 1:
                self.return_label.config(text="₱ 0.00")
            else:
                books.execute("SELECT sum(expected_profit) FROM bookinfos")
                return_ = sum(res[0] for res in books.fetchall())
                self.return_label.config(text="₱{:,.2f}".format(return_))

        def refresh_():
            delete_tree()
            show_info()
            self.search.set('')
            total_return()
            total_investment()

        # Refresh Button
        self.refresh = Image.open('refresh_2.png')
        self.refresh_render = ImageTk.PhotoImage(self.refresh)
        self.refresh_button = Button(self, image=self.refresh_render, command=refresh_, borderwidth=0)
        self.refresh_button.image = self.refresh_render
        self.refresh_button.place(x=450, y=110)

        def show_info():        
            books.execute("SELECT * FROM bookinfos")
    
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
                            data[6], data[7], data[8],
                            data[9], data[10]),
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
                            data[6], data[7], data[8],
                            data[9], data[10]),
                        tags=('oddrow',)
                    )
                i += 1
        
        show_info()

        def delete_tree():
            for i in self.tree_data.get_children():
                self.tree_data.delete(i)

        def add():

            self.add_frame = Frame(
                self,
                width=500,
                height=520,
                highlightbackground='black',
                highlightcolor='#87ceeb',
                highlightthickness=1,
                bg='white'
            )
            self.add_frame.place(x=450, y=100)

            self.import_button.config(state='disabled')
            self.export_button.config(state='disabled')
            self.search_entry.config(state='disabled', width=5)

            self.add_book_header = Image.open('add_book.png')
            self.add_book_header_render = ImageTk.PhotoImage(self.add_book_header)
            self.add_book_header_label = Label(self.add_frame, image=self.add_book_header_render)
            self.add_book_header_label.image = self.add_book_header_render
            self.add_book_header_label.place(x=0, y=0)

            def leave():
                answer = messagebox.askyesno("Confirmation", "Are you sure you want to exit?")
                if answer > 0:
                    self.import_button.config(state='normal')
                    self.export_button.config(state='normal')
                    self.search_entry.config(state='normal', width=41)
                    self.add_frame.destroy()

            # Exit Button
            self.exit_image = Image.open('exit.png')
            self.exit_image_render = ImageTk.PhotoImage(self.exit_image)
            self.exit_button = Button(
                self.add_frame,
                image=self.exit_image_render,
                borderwidth=0,
                command=leave,
                background='#87ceeb',
                activebackground='#87ceeb'
            )
            self.exit_button.image = self.exit_image_render
            self.exit_button.place(x=410, y=30)

            # Title
            self.title = StringVar()
            self.title_label = Label(self.add_frame, text="Title *", font=('Sans', 8, 'bold'), bg='white')
            self.title_label.place(x=50, y=100)
            self.title_entry = ttk.Entry(self.add_frame, textvariable=self.title, width=55, font=('Comfortaa', 10))
            self.title_entry.place(x=50, y=130)

            # Author
            self.author = StringVar()
            self.author_label = Label(self.add_frame, text="Author", font=('Sans', 8, 'bold'), bg='white')
            self.author_label.place(x=50, y=170)
            self.author_entry = ttk.Entry(self.add_frame, textvariable=self.author, width=55, font=('Comfortaa', 10))
            self.author_entry.place(x=50, y=200)

            # Publisher
            self.publisher = StringVar()
            self.publisher_label = Label(self.add_frame, text="Publisher", font=('Sans', 8, 'bold'), bg='white')
            self.publisher_label.place(x=50, y=240)
            self.publisher_entry = ttk.Entry(
                self.add_frame,
                textvariable=self.publisher,
                width=25,
                font=('Comfortaa', 10)
            )
            self.publisher_entry.place(x=50, y=270)

            # ISBN
            self.isbn = StringVar()
            self.isbn_label = Label(
                self.add_frame,
                text="ISBN",
                font=('Sans', 8, 'bold'),
                bg='white'
            )
            self.isbn_label.place(x=250, y=240)
            self.isbn_entry = ttk.Entry(
                self.add_frame,
                textvariable=self.isbn,
                width=26,
                justify='center',
                font=('Comfortaa', 10)
            )
            self.isbn_entry.place(x=250, y=270)

            # Quantity
            self.quantity = StringVar()
            self.quantity_label = Label(
                self.add_frame,
                text="Quantity *",
                font=('Sans', 8, 'bold'),
                bg='white'
            )
            self.quantity_label.place(x=50, y=310)
            self.quantity_entry = ttk.Entry(
                self.add_frame,
                textvariable=self.quantity,
                width=25,
                justify='center',
                font=('Comfortaa', 10)
            )
            self.quantity_entry.place(x=50, y=340)

            # Value of Item
            self.value_of_item = StringVar()
            self.value_of_item_label = Label(
                self.add_frame,
                text="Value of Item * ",
                font=('Sans', 8, 'bold'),
                bg='white'
            )
            self.value_of_item_label.place(x=250, y=310)
            self.value_of_item_entry = ttk.Entry(
                self.add_frame,
                textvariable=self.value_of_item,
                width=26,
                justify='center',
                font=('Comfortaa', 10)
            )
            self.value_of_item_entry.place(x=250, y=340)

            # Expected Profit
            self.expected_profit = StringVar()
            self.expected_profit_label = Label(
                self.add_frame,
                text="Expected Profit (%) *",
                font=('Sans', 8, 'bold'),
                bg='white'
            )
            self.expected_profit_label.place(x=50, y=380)
            self.expected_profit_entry = ttk.Entry(
                self.add_frame,
                textvariable=self.expected_profit,
                width=25,
                justify='center',
                font=('Comfortaa', 10)
            )
            self.expected_profit_entry.place(x=50, y=410)

            # Status
            status = [
                'AVAILABLE',
                'OUT OF STOCK',
                'SHIPPING'
            ]
            self.status = StringVar()
            self.status_label = Label(self.add_frame, text="Status *", font=('Sans', 8, 'bold'), bg='white')
            self.status_label.place(x=250, y=380)
            self.status_entry = ttk.Combobox(
                self.add_frame,
                state="readonly",
                values=list(status),
                textvariable=self.status,
                font=('Comfortaa', 10)
                )
            self.status_entry.place(x=250, y=410)
            self.status_entry.configure(width=24)
            self.status_entry.set('')

            def add_info():

                if self.status_entry.get() == '':
                    return messagebox.showerror('Ooops!', 'There was an error processing your data.')
                
                try:
                    int(self.quantity.get())
                    int(self.value_of_item.get())
                    int(self.expected_profit.get())

                    if (
                            int(self.quantity.get()) < 1
                            or int(self.value_of_item.get()) < 1
                            or int(self.expected_profit.get()) < 1
                    ):
                        return messagebox.showerror('Ooops!', 'There was an error processing your data.')

                except ValueError:
                    return messagebox.showerror('Ooops!', 'There was an error processing your data.')
                
                self.investment = round(int(self.quantity.get())*int(self.value_of_item.get()), 2)
                self.profit = round((self.investment*(int(self.expected_profit.get())/100))+self.investment, 2)
                
                books.execute("""INSERT into bookinfos (
                                title, author, publisher, isbn, 
                                quantity, value, profit, status, investment, 
                                expected_profit) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                    self.title.get(),
                    self.author.get(),
                    self.publisher.get(),
                    self.isbn.get(),
                    self.quantity.get(),
                    self.value_of_item.get(),
                    self.expected_profit.get(),
                    self.status_entry.get().upper(),
                    self.investment,
                    self.profit
                    ))

                book_con.commit()

                self.title.set('')
                self.author.set('')
                self.publisher.set('')
                self.isbn.set('')
                self.quantity.set('')
                self.value_of_item.set('')
                self.status.set('')
                self.expected_profit.set('')

                delete_tree()
                show_info() 
                total_return()
                total_investment()

                self.import_button.config(state='normal')
                self.export_button.config(state='normal')
                self.search_entry.config(state='normal', width=41)

                self.add_frame.destroy()

                return messagebox.showinfo('Added Successfully', 'Your entries have been added')

            # Add Button
            self.add_button_image = Image.open('submit.png')
            self.add_button_render = ImageTk.PhotoImage(self.add_button_image)
            self.add_button = Button(
                self.add_frame,
                image=self.add_button_render,
                borderwidth=0,
                command=add_info,
                bg='white',
                activebackground='white'
            )
            self.add_button.image = self.add_button_render
            self.add_button.place(x=170, y=460)

            def refresh():
                self.title.set('')
                self.author.set('')
                self.publisher.set('')
                self.isbn.set('')
                self.quantity.set('')
                self.value_of_item.set('')
                self.status.set('')
                self.expected_profit.set('')

            # Refresh Button
            self.refresh_image = Image.open('refresh.png')
            self.refresh_image_render = ImageTk.PhotoImage(self.refresh_image)
            self.refresh_button = Button(
                self.add_frame,
                image=self.refresh_image_render,
                borderwidth=0,
                command=refresh,
                background='white',
                activebackground='white'
            )
            self.refresh_button.image = self.refresh_image_render
            self.refresh_button.place(x=410, y=460)

        def select_data():

            if not self.tree_data.selection():
                return messagebox.showerror('No Entries Found', 'It seems like there are no selected entry yet.')

            self.selected_item = self.tree_data.focus()
            self.values = self.tree_data.item(self.selected_item, 'values')

            self.update_frame = Frame(
                self,
                width=500,
                height=520,
                highlightbackground='black',
                highlightcolor='#87ceeb',
                highlightthickness=1,
                bg='white'
            )
            self.update_frame.place(x=441, y=100)

            self.update_book_header = Image.open('add_book.png')
            self.update_book_header_render = ImageTk.PhotoImage(self.update_book_header)
            self.update_book_header_img = Label(self.update_frame, image=self.update_book_header_render)
            self.update_book_header_img.image = self.update_book_header_render
            self.update_book_header_img.place(x=0, y=0)

            self.import_button.config(state='disabled')
            self.export_button.config(state='disabled')
            self.search_entry.config(state='disabled', width=5)

            def leave():
                answer = messagebox.askyesno("Confirmation", "Are you sure you want to exit?")
                if answer > 0:
                    self.import_button.config(state='normal')
                    self.export_button.config(state='normal')
                    self.search_entry.config(state='normal', width=41)

                    self.update_frame.destroy()

            # Exit Button
            self.exit_image = Image.open('exit.png')
            self.exit_image_render = ImageTk.PhotoImage(self.exit_image)
            self.exit_button = Button(
                self.update_frame,
                image=self.exit_image_render,
                borderwidth=0,
                command=leave,
                background='#87ceeb',
                activebackground='#87ceeb'
            )
            self.exit_button.image = self.exit_image_render
            self.exit_button.place(x=410, y=30)

            # Title
            self.title = StringVar()
            self.title_label = Label(self.update_frame, text="Title *", font=('Sans', 8, 'bold'), bg='white')
            self.title_label.place(x=50, y=100)
            self.title_entry = ttk.Entry(self.update_frame, textvariable=self.title, width=55, font=('Comfortaa', 10))
            self.title_entry.place(x=50, y=130)

            # Author
            self.author = StringVar()
            self.author_label = Label(self.update_frame, text="Author", font=('Sans', 8, 'bold'), bg='white')
            self.author_label.place(x=50, y=170)
            self.author_entry = ttk.Entry(self.update_frame, textvariable=self.author, width=55, font=('Comfortaa', 10))
            self.author_entry.place(x=50, y=200)

            # Publisher
            self.publisher = StringVar()
            self.publisher_label = Label(self.update_frame, text="Publisher", font=('Sans', 8, 'bold'), bg='white')
            self.publisher_label.place(x=50, y=240)
            self.publisher_entry = ttk.Entry(
                self.update_frame,
                textvariable=self.publisher,
                width=25,
                font=('Comfortaa', 10)
            )
            self.publisher_entry.place(x=50, y=270)

            # ISBN
            self.isbn = StringVar()
            self.isbn_label = Label(
                self.update_frame,
                text="ISBN",
                font=('Sans', 8, 'bold'),
                bg='white'
            )
            self.isbn_label.place(x=250, y=240)
            self.isbn_entry = ttk.Entry(
                self.update_frame,
                textvariable=self.isbn,
                width=26,
                justify='center',
                font=('Comfortaa', 10)
            )
            self.isbn_entry.place(x=250, y=270)

            # Quantity
            self.quantity = StringVar()
            self.quantity_label = Label(
                self.update_frame,
                text="Quantity *",
                font=('Sans', 8, 'bold'),
                bg='white'
            )
            self.quantity_label.place(x=50, y=310)
            self.quantity_entry = ttk.Entry(
                self.update_frame,
                textvariable=self.quantity,
                width=25,
                justify='center',
                font=('Comfortaa', 10)
            )
            self.quantity_entry.place(x=50, y=340)

            # Value of Item
            self.value_of_item = StringVar()
            self.value_of_item_label = Label(
                self.update_frame,
                text="Value of Item *",
                font=('Sans', 8, 'bold'),
                bg='white'
            )
            self.value_of_item_label.place(x=250, y=310)
            self.value_of_item_entry = ttk.Entry(
                self.update_frame,
                textvariable=self.value_of_item,
                width=26,
                justify='center',
                font=('Comfortaa', 10)
            )
            self.value_of_item_entry.place(x=250, y=340)
            
            # Expected Profit
            self.expected_profit = StringVar()
            self.expected_profit_label = Label(
                self.update_frame,
                text="Expected Profit (%) *",
                font=('Sans', 8, 'bold'),
                bg='white'
            )
            self.expected_profit_label.place(x=50, y=380)
            self.expected_profit_entry = ttk.Entry(
                self.update_frame,
                textvariable=self.expected_profit,
                width=25,
                justify='center',
                font=('Comfortaa', 10)
            )
            self.expected_profit_entry.place(x=50, y=410)

            # Status
            status = [
                'AVAILABLE',
                'OUT OF STOCK',
                'SHIPPING'
            ]
            self.status = StringVar()
            self.status_label = Label(self.update_frame, text="Status *", font=('Sans', 8, 'bold'), bg='white')
            self.status_label.place(x=250, y=380)
            self.status_entry = ttk.Combobox(
                self.update_frame,
                state="readonly",
                values=list(status),
                textvariable=self.status,
                font=('Comfortaa', 10)
                )
            self.status_entry.place(x=250, y=410)
            self.status_entry.configure(width=24)
            self.status_entry.set('')

            self.title_entry.insert(0, self.values[1])
            self.author_entry.insert(0, self.values[2])
            self.publisher_entry.insert(0, self.values[3])
            self.isbn_entry.insert(0, self.values[4])
            self.quantity_entry.insert(0, self.values[5])
            self.value_of_item_entry.insert(0, self.values[6])
            self.expected_profit_entry.insert(0, self.values[7])
            self.status_entry.set(self.values[8])

            def update_record():

                self.selected_item = self.tree_data.focus()
                self.tree_data.item(
                    self.selected_item, 
                    text='', 
                    values=(
                        self.title_entry.get(),
                        self.author_entry.get(),
                        self.publisher_entry.get(),
                        self.isbn_entry.get(),
                        self.quantity_entry.get(),
                        self.value_of_item_entry.get(),
                        self.expected_profit_entry.get(),
                        self.status_entry.get()
                    )
                )

                try:
                    int(self.quantity.get())
                    int(self.value_of_item.get())
                    int(self.expected_profit.get())

                    if (
                            int(self.quantity.get()) < 1
                            or int(self.value_of_item.get()) < 1
                            or int(self.expected_profit.get()) < 1):
                        return messagebox.showerror('Ooops!', 'There was an error processing your data.')
                        
                except ValueError:
                    return messagebox.showerror('Ooops!', 'There was an error processing your data.')

                self.investment = round(int(self.quantity.get())*int(self.value_of_item.get()), 2)
                self.profit = round((self.investment*(int(self.expected_profit.get())/100))+self.investment, 2)

                books.execute("""UPDATE bookinfos SET 
                                title=?, author=?, publisher=?, 
                                isbn=?, quantity=?, value=?, 
                                profit=?, status=?, investment=?, expected_profit=? 
                                WHERE book_id=?""", (
                    self.title.get(),
                    self.author.get(),
                    self.publisher.get(),
                    self.isbn.get(),
                    self.quantity.get(),
                    self.value_of_item.get(),
                    self.expected_profit.get(),
                    self.status.get(),
                    self.investment,
                    self.profit,
                    self.values[0]
                    ))

                book_con.commit()

                self.title.set('')
                self.author.set('')
                self.publisher.set('')
                self.isbn.set('')
                self.quantity.set('')
                self.value_of_item.set('')
                self.expected_profit.set('')
                self.status.set('')

                delete_tree()
                show_info()
                total_return()
                total_investment()

                self.import_button.config(state='normal')
                self.export_button.config(state='normal')
                self.search_entry.config(state='normal', width=41)

                self.update_frame.destroy()
                
                return messagebox.showinfo('Updated Successfully', 'Your entries have been updated')

            # Add Button
            self.update_image = Image.open('submit.png')
            self.update_image_render = ImageTk.PhotoImage(self.update_image)
            self.update_button = Button(
                self.update_frame,
                image=self.update_image_render,
                borderwidth=0,
                command=update_record,
                bg='white',
                activebackground='white'
            )
            self.update_button.image = self.update_image_render
            self.update_button.place(x=170, y=460)

            def refresh():
                self.title.set('')
                self.author.set('')
                self.publisher.set('')
                self.isbn.set('')
                self.quantity.set('')
                self.value_of_item.set('')
                self.expected_profit.set('')
                self.status.set('')

            # Refresh Button
            self.refresh_image = Image.open('refresh.png')
            self.refresh_image_render = ImageTk.PhotoImage(self.refresh_image)
            self.refresh_button = Button(
                self.update_frame,
                image=self.refresh_image_render,
                borderwidth=0,
                command=refresh,
                background='white',
                activebackground='white'
            )
            self.refresh_button.image = self.refresh_image_render
            self.refresh_button.place(x=410, y=460)

        # Remove Function for TreeView and Database
        def remove_record():
            if not self.tree_data.selection():
                return messagebox.showerror('No Entries Found', 'It seems like there are no entries given yet.')

            answer = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected item/s?")
            if answer > 0:
                data = self.tree_data.selection()
                for data in data:
                    uid = self.tree_data.item(data)['values'][0]  # Book ID

                    books.execute("DELETE FROM bookinfos WHERE book_id=?", (uid,))
                    self.tree_data.delete(data)

                refresh_()

                book_con.commit()

                return messagebox.showinfo("Deleted Successfully", "The book Information has been deleted.")

        # Delete Button
        self.trash = Image.open('trash.png')
        self.trash_render = ImageTk.PhotoImage(self.trash)
        self.delete_button = Button(self, image=self.trash_render, command=remove_record, borderwidth=0)
        self.delete_button.image = self.trash_render
        self.delete_button.place(x=680, y=189)

        # Update Button
        self.edit_image = Image.open('edit.png')
        self.edit_image_render = ImageTk.PhotoImage(self.edit_image)
        self.edit_button = Button(self, image=self.edit_image_render, borderwidth=0, command=select_data)
        self.edit_button.image = self.edit_image_render
        self.edit_button.place(x=510, y=189)

        # Add Button
        self.add_image = Image.open('add.png')
        self.add_image_render = ImageTk.PhotoImage(self.add_image)
        self.add_button = Button(self, image=self.add_image_render, command=add, borderwidth=0)
        self.add_button.image = self.add_image_render
        self.add_button.place(x=350, y=189)

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
                            isbn, quantity, value, profit, 
                            status, investment, expected_profit
                            FROM bookinfos 
                            WHERE author LIKE ? OR title LIKE ?""", (
                '%' + searching + '%',
                '%' + searching + '%')
            )
            rows = books.fetchall()
            book_con.commit()
            update(rows)

        # Search Entry
        self.search = StringVar()
        self.search_entry = Entry(
            self,
            textvariable=self.search,
            width=41,
            font=('Comfortee', 10),
            borderwidth=0,
            selectbackground='skyblue'
        )
        self.search_entry.place(x=770, y=203)
        self.search_entry.bind("<KeyRelease>", search)

        # Importing CSV
        def importcsv():
            fln = filedialog.askopenfilename(
                initialdir=os.getcwd(),
                title="Open CSV",
                filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
            )
            if fln == '':
                return messagebox.showinfo('Unknown Directory', 'There are no file to be imported.')

            with open(fln, errors="ignore") as myfile:
                self.csvread = csv.reader(myfile, delimiter=',')
                for i in self.csvread:
                    update(self.csvread)

            for i in self.tree_data.get_children():
                data = self.tree_data.item(i)["values"]
                title = data[1]
                author = data[2]
                publisher = data[3]
                isbn = data[4]
                quantity = data[5]
                value = data[6]
                profit_percent = data[7]
                status = data[8]
                investment = data[9]
                profit = data[10]

                books.execute("""INSERT into bookinfos (
                            title, author, publisher, isbn, 
                            quantity, value, profit, status, investment, 
                            expected_profit) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                    title,
                    author,
                    publisher,
                    isbn,
                    quantity,
                    value,
                    profit_percent,
                    status,
                    investment,
                    profit
                ))

            book_con.commit()

            delete_tree()
            show_info()
            total_return()
            total_investment()

            return messagebox.showinfo('Imported Successfully',
                                       'The content of the CSV file has been added to the application.')

        # Import Button
        self.import_ = Image.open('import.png')
        self.import_render = ImageTk.PhotoImage(self.import_)
        self.import_button = Button(self, image=self.import_render, command=importcsv, borderwidth=0)
        self.import_button.image = self.import_render
        self.import_button.place(x=190, y=189)

        def exportcsv():
            if len(self.tree_data.get_children()) < 1:
                return messagebox.showinfo('Data not Found', 'There are no data to be exported.')

            fln = filedialog.asksaveasfilename(
                initialdir=os.getcwd(),
                title="Save CSV",
                filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
            )

            if fln == '':
                return messagebox.showinfo('Unknown Directory', 'There are no file to be exported.')

            with open(fln, 'w', newline='') as myfile:
                exp_writer = csv.writer(myfile, delimiter=",")
                exp_writer.writerow(
                    [
                        'book_ud', 'title', 'author',
                        'publisher', 'isbn', 'quantity',
                        'value', 'profit_percent', 'status',
                        'investment', 'expected_profit'])
                for i in (self.tree_data.get_children()):
                    data = self.tree_data.item(i)["values"]
                    exp_writer.writerow(data)

            return messagebox.showinfo('Exported Successfully',
                                       ' The information has been exported successfully')

        # Export Button
        self.export = Image.open('export.png')
        self.export_render = ImageTk.PhotoImage(self.export)
        self.export_button = Button(self, image=self.export_render, command=exportcsv, borderwidth=0)
        self.export_button.image = self.export_render
        self.export_button.place(x=30, y=189)
