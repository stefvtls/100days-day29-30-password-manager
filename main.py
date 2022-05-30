import tkinter
from tkinter import messagebox
import random
import json
# import pyperclip

# PASSWORD GENERATOR #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_list = [random.choice(letters) for char in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for char in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for char in range(random.randint(2, 4))]
    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    # pyperclip.copy(password)


# END OF PASSWORD GENERATOR#


window = tkinter.Tk()
window.title("Password Manager")
window.minsize(width=220, height=220)
window.config(padx=40, pady=40)

canvas = tkinter.Canvas(width=200, height=200, highlightthickness=0)
photoimage = tkinter.PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=photoimage)
canvas.grid(row=0, column=1)

website = tkinter.Label(text="Website:")
website.grid(row=1, column=0)
email = tkinter.Label(text="Email/Username:")
email.grid(row=2, column=0)
password = tkinter.Label(text="Password:")
password.grid(row=3, column=0)

website_entry = tkinter.Entry(width=32)
website_entry.grid(column=1, row=1)

email_entry = tkinter.Entry(width=50)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.focus()
email_entry.insert("end", "@gmail.com")

password_entry = tkinter.Entry(width=32)
password_entry.grid(column=1, row=3)


def save():
    website_ent = website_entry.get()
    email_ent = email_entry.get()
    password_ent = password_entry.get()
    ent = {website_ent: {"email": email_ent, "password": password_ent}}


    if len(website_ent) != 0 and len(email_ent) > 10 and len(password_ent) != 0:
        okcancel = tkinter.messagebox.askokcancel(title=f"save a new entry for {website_ent}", message=f"the entries "
                                                                                                       f"are: \n "
                                                                                                       f"login: "
                                                                                                       f"{email_ent} "
                                                                                                       f"\n password: "
                                                                                                       f"{password_ent}. \n Save it?")
        if okcancel:
            try:
                with open("data.json", "r") as file:
                    saved = json.load(file)
            except FileNotFoundError:
                with open("data.json", "w") as file:
                    json.dump(ent, file, indent=4)
            else:
                saved.update(ent)
                with open("data.json", "w") as file:
                    json.dump(saved, file, indent=4)
            finally:
                website_entry.delete(0, "end")
                email_entry.delete(0, "end")
                email_entry.insert("end", "@gmail.com")
                password_entry.delete(0, "end")
    else:
        tkinter.messagebox.showinfo(title="cannot save the entry", message="you ommited one or more entries. fill all "
                                                                           "the entries to save")


def search_in_entries():
    website_ent = website_entry.get()
    try:
        with open("data.json", "r") as file:
            stored_passwords = json.load(file)
            log_in = stored_passwords[str(website_ent)]["email"]
            login_password = stored_passwords[str(website_ent)]["password"]
    except FileNotFoundError:
        tkinter.messagebox.showinfo(title="no entries", message="no entries saved yet. No data file found")
    except KeyError:
        tkinter.messagebox.showinfo(title="no entries", message="no entries saved yet. No details for the website "
                                                                "exists.")
    else:
        tkinter.messagebox.showinfo(title=f"entries for {website_ent}", message=f"your login is: {log_in} "
                                                                                f"\n your password is: {login_password}")


generate_button = tkinter.Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)
add_button = tkinter.Button(text="Add", width=43, command=save)
add_button.grid(column=1, columnspan=2, row=4)
search_button = tkinter.Button(text="Search", width=14, command=search_in_entries)
search_button.grid(column=2, row=1)

window.mainloop()
