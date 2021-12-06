from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_numbers = random.randint(2, 4)
    nr_symbols = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list = password_letters + password_numbers + password_symbols

    random.shuffle(password_list)
    password_str = "".join(password_list)
    password.insert(0, password_str)
    pyperclip.copy(password_str)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website_entered = website.get()
    email_entered = email.get()
    password_entered = password.get()

    new_data = {
        website_entered: {
            "email": email_entered,
            "password": password_entered,
        }
    }

    if website_entered == "" or email_entered == "" or password_entered == "":
        messagebox.showerror(title="Error", message="No Fields can be left empty")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"The email is {email_entered}\n Password is"
                                                              f" {password_entered}\n Is it ok to save ? ")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website.delete(0, END)
                email.delete(0, END)
                password.delete(0, END)
        else:
            website.delete(0, END)
            email.delete(0, END)
            password.delete(0, END)
# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    website_entered = website.get()
    with open("data.json") as data_file:
        data = json.load(data_file)
        if website_entered in data:
            o_email = data[website_entered]['email']
            o_password = data[website_entered]['password']
            messagebox.showinfo(title=website_entered, message=f"Email: {o_email}\nPassword: {o_password}")
        else:
            messagebox.showerror(title="Error", message="No such website in data")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=300, height=300)
logo = PhotoImage(file="logo.png")
canvas.create_image(150, 150, image=logo)
canvas.grid(column=0, row=0, columnspan=3)

web_label = Label(text="Website:", font=("Arial", 12, "bold"))
web_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:", font=("Arial", 12, "bold"))
email_label.grid(column=0, row=2)
pass_label = Label(text="Password:", font=("Arial", 12, "bold"))
pass_label.grid(column=0, row=3)

website = Entry()
website.grid(column=1, row=1)
website.config(width=21)
website.focus()

search = Button(text="Search", command=find_password)
search.config(width=13)
search.grid(column=2, row=1)

email = Entry()
email.grid(column=1, row=2, columnspan=2)
email.config(width=35)

password = Entry()
password.config(width=21)
password.grid(column=1, row=3)

button = Button(text="Generate Password", command=password_generator)
button.grid(column=2, row=3)
add = Button(text="Add", command=save_password)
add.config(width=36)
add.grid(column=1, row=4, columnspan=2)

canvas.mainloop()
