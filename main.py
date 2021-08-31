from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
               "t", "u", "v", "w", "x", "y", "z"]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['#', '$', '%', '&', '/', '(', ')', '=', '?', '¿', '¡', '!', '+', '*']

    password_numbers = [choice(numbers) for char in range(randint(2, 4))]
    password_letters = [choice(letters) for char in range(randint(8, 10))]
    password_symbols = [choice(symbols) for char in range(randint(2, 4))]
    password_list = password_letters + password_numbers + password_symbols
    print(f"password list: {len(password_list)}")
    shuffle(password_list)

    password_generated = "".join(password_list)
    print(f"password generated: {len(password_generated)}")
    password_entry.delete(0, END)
    password_entry.insert(0, password_generated)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    new_data = {
        website_entry.get(): {
            "email:": email_entry.get(),
            "password:": password_entry.get(),
        }
    }
    #Si ningún campo está vacío:
    if len(website_entry.get()) > 0 and len(email_entry.get()) > 0 and len(password_entry.get()) > 0:
        #Confirma si los datos son correctos:
        datos_correctos = messagebox.askokcancel(title="Revisión de datos", message=f"Sitio Web: {website_entry.get()}\n"
                                                                                    f"Correo electronico: {email_entry.get()}\n"
                                                                                    f"Contraseña: {password_entry.get()}\n "
                                                                                    f"¿Son estos datos correctos?")  # Crea una pestaña que aparece
        if datos_correctos:
            #Intenta abrir el archivo y leerlo:
            try:
                with open ("data.json", mode="r") as data_file:
                    data = json.load(data_file)

            #Si el archivo no se encuentra crealo con la informacion:
            except FileNotFoundError:
                with open("data.json", mode="w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            #sin embargo si el archivo si se encuentra actualizalo con la nueva informacion:
            else:
                data.update(new_data)

                with open("data.json", mode="w") as data_file:  # El modo a es por append, añadir
                    json.dump(data, data_file, indent=4)
            #Finalmente. No importa que pase, ponlo todo en blanco
            finally:
                website_entry.delete(0, END)
                email_entry.delete(0, END)
                password_entry.delete(0, END)
    #Si algún campo de texto está vacío:
    else:
        messagebox.showinfo(title="Campo vacío", message="No dejes ningún campo vacío")

# ---------------------------- SEARCH ------------------------------- #

def search ():
    try:
        with open("data.json", mode="r") as archive:
            readed_archive = json.load(archive)
    except FileNotFoundError:
        messagebox.showinfo(title="No hay datos aun", message="Parece que este programa es nuevo y no se le han ingresado datos")
    else:
        password_found = [value for (key, value) in readed_archive.items() if website_entry.get() == key ]
        print(password_found)
        if len(password_found) > 0:
            messagebox.showinfo(title="Esto fue lo que encontramos", message= f"Sitio Web: {website_entry.get()}\nCorreo electrónico: {password_found[0]['email:']}\nContraseña: {password_found[0]['password:']}")
        else:
            messagebox.showinfo(title="No existen datos de este sitio web", message= f"No pudimos encontrar datos del sitio:\n   {website_entry.get()}\nAsegurate de haber escrito bien el sitio")
# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)
photo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=photo)
canvas.grid(column=1, row=0)

websitelabel = Label(text="Website:")
websitelabel.grid(column=0, row=1)
website_entry = Entry(width=35)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=2)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_entry = Entry(width=35)
password_entry.grid(column=1, row=3, columnspan=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

password_button = Button(text="Generate Password", command=password_generator)
password_button.grid(column=2, row=3)

search_button = Button (text= "Search", command= search)
search_button.grid(column=2, row=1)
window.mainloop()

