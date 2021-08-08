# Log In and Sign Up Screen
from tkinter import *
from tkinter import messagebox
import sqlite3
from PIL import ImageTk, Image
from tkinter import ttk
import hashlib

# User's Database
data_con = sqlite3.connect('userdb.db')

users = data_con.cursor()


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        front = Image.open('front.png')
        render = ImageTk.PhotoImage(front)
        img = Label(self, image=render)
        img.image = render
        img.place(x=320, y=5)

        # Username
        self.username = StringVar()
        self.usernameEntry = Entry(self, width=31, textvariable=self.username, font=("Roboto", 14), borderwidth=0)
        self.usernameEntry.place(x=515, y=182)

        # Password
        self.password = StringVar()
        self.passwordEntry = Entry(
            self,
            width=30,
            textvariable=self.password,
            show='*',
            font=("Roboto", 14),
            borderwidth=0
        )
        self.passwordEntry.place(x=515, y=340)

        # Store Function
        def login():
            if self.username.get() == '' or self.password.get() == '':
                return messagebox.showerror('Insufficient Entries', 'Please fill-up all the  required information.')
            else:

                if self.username.get() == 'GAZE-Admin' and self.password.get() == 'admingaze':
                    self.username.set('')
                    self.password.set('')
                    controller.show_frame("Admin")
                else:

                    passw = self.password.get().encode()
                    md5_object = hashlib.md5()
                    md5_object.update(passw)
                    encrpyted_password = md5_object.hexdigest()

                    users.execute("SELECT username, password FROM users")

                    for (username, password) in users:
                        if self.username.get() == username and encrpyted_password == password:
                            self.username.set('')
                            self.password.set('')
                            controller.show_frame("User")
                            return messagebox.showinfo('Logged In Successfully', 'Log In Successfully')
                    self.password.set('')
                    return messagebox.showerror('Logging In Failed', 'Incorrect email or password.')

        # LogIn Button
        log_in = Image.open('login.png')
        render = ImageTk.PhotoImage(log_in)
        self.login_button = Button(
            self,
            image=render,
            borderwidth=0,
            command=login,
            bg="#87ceeb",
            activebackground='#87ceeb')
        self.login_button.image = render
        self.login_button.place(x=465, y=450)

        def signup():

            self.signup_frame = Frame(
                self,
                width=400,
                height=420,
                highlightbackground='black',
                highlightcolor='#87ceeb',
                highlightthickness=1,
                bg='white'
            )
            self.signup_frame.place(x=491, y=130)

            self.signup_button.config(state='disabled')
            self.usernameEntry.config(state='disabled')
            self.passwordEntry.config(state='disabled')

            # Sign Up Header
            self.sign_up_header = Image.open('signup_header.png')
            self.sign_up_header_render = ImageTk.PhotoImage(self.sign_up_header)
            self.sign_up_img = Label(self.signup_frame, image=self.sign_up_header_render)
            self.sign_up_img.image = self.sign_up_header_render
            self.sign_up_img.place(x=0, y=0)

            # Exit Function for Sign Up Frame
            def leave():
                self.signup_frame.destroy()
                self.signup_button.config(state='normal')
                self.usernameEntry.config(state='normal')
                self.passwordEntry.config(state='normal')

            # Exit Button
            self.exit_image = Image.open('exit.png')
            self.exit_image_render = ImageTk.PhotoImage(self.exit_image)
            self.exit_button = Button(
                self.signup_frame,
                image=self.exit_image_render,
                borderwidth=0,
                command=leave,
                background='#87ceeb',
                activebackground='#87ceeb'
            )
            self.exit_button.image = self.exit_image_render
            self.exit_button.place(x=350, y=30)

            # Create a username
            self.label_create_username = Label(
                self.signup_frame,
                text="Username",
                font=("Sans", 8, 'bold'),
                background='white'
            )
            self.label_create_username.place(x=75, y=125)
            self.create_username = StringVar()
            self.create_usernameEntry = ttk.Entry(
                self.signup_frame,
                width=35,
                textvariable=self.create_username,
                font=("Comfortaa", 10)
            )
            self.create_usernameEntry.place(x=75, y=150)

            # Create a password
            self.label_create_password = Label(
                self.signup_frame,
                text="Password",
                font=("Sans", 8, 'bold'),
                background='white'
            )
            self.label_create_password.place(x=75, y=200)
            self.create_password = StringVar()
            self.create_passwordEntry = ttk.Entry(
                self.signup_frame,
                width=35,
                textvariable=self.create_password,
                show='*',
                font=("Comfortaa", 10)
            )
            self.create_passwordEntry.place(x=75, y=225)

            # Confirm a password
            self.label_confirm_password = Label(
                self.signup_frame,
                text="Confirm Password",
                font=("Sans", 8, 'bold'),
                background='white'
            )
            self.label_confirm_password.place(x=75, y=275)
            self.confirm_password = StringVar()
            self.confirm_passwordEntry = ttk.Entry(
                self.signup_frame,
                width=35,
                textvariable=self.confirm_password,
                show='*',
                font=("Comfortaa", 10)
            )
            self.confirm_passwordEntry.place(x=75, y=300)

            # Submit Function
            def submit():

                if (self.create_username.get() == ''
                        or self.create_password.get() == ''
                        or self.confirm_password.get() == ''):
                    return messagebox.showerror('No Data Found',
                                                'Kindly fill-out the information.')

                if self.create_password.get() != self.confirm_password.get():
                    return messagebox.showerror('Password ERROR', 'The password you entered does not match.')

                users.execute("SELECT username from Users")

                self.myusernames = (res[0] for res in users.fetchall())

                if self.create_username.get() in self.myusernames:
                    return messagebox.showinfo('Unavailable', 'The username you entered is already in used.')

                users.execute("SELECT username from Users")

                self.myusernames = (res[0] for res in users.fetchall())

                if self.create_username.get() in self.myusernames:
                    return messagebox.showinfo('Unavailable', 'The username you entered is already in used.')

                if (self.create_username.get() not in self.myusernames
                        and self.create_password.get() == self.confirm_password.get()):

                    passw = self.create_password.get().encode()
                    md5_object = hashlib.md5()
                    md5_object.update(passw)
                    password = md5_object.hexdigest()

                    users.execute("INSERT into users (username, password) values(?, ?)", (
                        self.create_username.get(),
                        password
                        ))

                    data_con.commit()

                    self.create_password.set('')
                    self.confirm_password.set('')
                    self.create_username.set('')

                    self.signup_button.config(state='normal')
                    self.usernameEntry.config(state='normal')
                    self.passwordEntry.config(state='normal')

                    self.signup_frame.destroy()

                    return messagebox.showinfo('Registration Successful', 'Your entries have been submitted')

            # Submit Button
            self.submit_image = Image.open('submit.png')
            self.submit_image_render = ImageTk.PhotoImage(self.submit_image)
            self.submit_image_button = Button(
                self.signup_frame,
                image=self.submit_image_render,
                borderwidth=0,
                command=submit,
                bg='white',
                activebackground='white'
            )
            self.submit_image_button.image = self.submit_image_render
            self.submit_image_button.place(x=130, y=350)

        # Signup Button
        sign_up = Image.open('signup.png')
        render = ImageTk.PhotoImage(sign_up)
        self.signup_button = Button(
            self, image=render,
            borderwidth=0,
            bg="#87ceeb",
            activebackground='#87ceeb',
            command=signup
        )
        self.signup_button.image = render
        self.signup_button.place(x=725, y=574)
