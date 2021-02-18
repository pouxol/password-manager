from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


def search():
    cur_website = website_entry.get()
    with open("pw_database.json", mode="r") as file:
        data = json.load(file)

        if cur_website in data:
            cur_pw = data[cur_website]["password"]
            cur_eu = data[cur_website]["email"]
            messagebox.showinfo(title=f"Your credentials for {cur_website}", message=f"Email: {cur_eu} \nPassword: {cur_pw}")
        else:
            messagebox.showinfo(title=f"Error", message=f"There are no credentials for {cur_website}")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_pw():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_letters = [choice(letters) for _ in range(nr_letters)]
    password_symbols = [choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password_gen = "".join(password_list)

    password_entry.insert(0, password_gen)
    pyperclip.copy(password_gen)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add():
    cur_website = website_entry.get()
    cur_eu = eu_entry.get()
    cur_pw = password_entry.get()
    new_data = {
        cur_website: {"email": cur_eu,
                      "password": cur_pw
                      }
    }

    if cur_website == "" or cur_eu == "" or cur_pw == "":
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=cur_website,
                                       message=f"These are the details you entered: "
                                               f"\nEmail: {cur_eu} \nPassword: {cur_pw} \nIs it ok to save?")

        if is_ok:
            try:
                with open("pw_database.json", mode="r") as file:
                    data = json.load(file)

            except FileNotFoundError:
                with open("pw_database.json", mode="w") as file:
                    json.dump(new_data, file, indent=4)

            else:
                data.update(new_data)

                with open("pw_database.json", mode="w") as file:
                    json.dump(data, file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

website = Label(text="Website:")
website.grid(row=1, column=0)

website_entry = Entry()
website_entry.grid(row=1, column=1)
website_entry.focus()
website_entry.get()

eu = Label(text="Email/Username:")
eu.grid(row=2, column=0)

eu_entry = Entry(width=38)
eu_entry.grid(row=2, column=1, columnspan=2)
eu_entry.insert(0, "YOUR_MAIL_ADDRESS")
eu_entry.get()

password = Label(text="Password:")
password.grid(row=3, column=0)

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1)
password_entry.get()

button_password = Button(text="Generate Password", command=generate_pw)
button_password.grid(row=3, column=2)

button_add = Button(text="Add", command=add, width=36)
button_add.grid(row=4, column=1, columnspan=2)

button_search = Button(text="Search", command=search)
button_search.grid(row=1, column=2)

window.mainloop()
