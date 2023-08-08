from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import requests
import hashlib

data_file = "D:\Zohaib Tahir\PyCharm Project\Password Manager\data.json"
logo = "D:\Zohaib Tahir\PyCharm Project\Password Manager\logo.png"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    passcode = "".join(password_list)
    password_input.insert(0, passcode)
    pyperclip.copy(passcode)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if website == "" or password == "":
        messagebox.showinfo(title="Error", message="Please fill all fields")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details \nEmail: {email}"
                                                              f"\n Password: {password} \n Is it ok to save it?")

        if is_ok:
            try:
                with open(data_file, "r") as file:
                    # reading old data
                    data = json.load(file)
            except FileNotFoundError:
                with open(data_file, "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                # updating old data with new data
                data.update(new_data)

                with open(data_file, "w") as file:
                    # saving updated data
                    json.dump(data, file, indent=4)
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)


# ---------------------------- RETRIEVE DATA ------------------------------- #
def data_retrieve():
    website = website_input.get().title()
    password = password_input.get()
    try:
        with open(data_file, "r") as file:
            data = json.load(file)
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title="Password Information", message=f"Email: {email}\nPassword: {password}")
            else:
                messagebox.showinfo(title="Error", message="No details exist for this Website.")
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")


# PASSWORD VALIDATOR
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    password = password_input.get()
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def main():
    password = password_input.get()
    for _ in password:
        count = pwned_api_check(password)
        if count:
            messagebox.showwarning(title="Warning", message=f"{password} was found {count} times... "
                                                            f" Maybe you should change your password")
            break
        else:
            messagebox.showinfo(title="Congratulations", message=f'{password} was not found. Carry on!')
            break
    return 'done!'


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="#f7f5dd")

canvas = Canvas(width=200, height=200, bg="#f7f5dd", highlightthickness=0)
img = PhotoImage(file=logo)
canvas.create_image(100, 100, image=img)
canvas.grid(column=1, row=0)

# Labels
label_1 = Label(text="Website:", bg="#f7f5dd")
label_1.grid(column=0, row=1)
label_2 = Label(text="E-Mail/Username:", bg="#f7f5dd")
label_2.grid(column=0, row=2)
label_3 = Label(text="Password:", bg="#f7f5dd")
label_3.grid(column=0, row=3)

# Entry
website_input = Entry(width=35)
website_input.grid(column=1, row=1)
website_input.focus()
email_input = Entry(width=35)
email_input.grid(column=1, row=2)
email_input.insert(0, "zohaibtahir2011@gmail.com")
password_input = Entry(width=21)
password_input.grid(column=1, row=3)

# Button
button_1 = Button(text="Generate Password", command=password_generator)
button_1.grid(column=2, row=3)
button_2 = Button(text="Add", width=36, command=save)
button_2.grid(column=0, row=4, columnspan=3)
button_3 = Button(text="Search", command=data_retrieve)
button_3.grid(column=2, row=1)
button_3 = Button(text="Check", command=main)
button_3.grid(column=2, row=4)

window.mainloop()
