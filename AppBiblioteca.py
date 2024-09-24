import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import pymysql

class DataBaseManager():
    ##conection to DB MySQL
    def __init__(self):
        self.connection = pymysql.connect(host='localhost', user='root', password='root', db='biblioteca')
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()


##Here starts Class USERS##
class Users():
    def __init__(self, root, db_manager):
        self.db_manager = db_manager
        self.root = tk.Tk()
        self.root.title('Gestión de usuarios')
        self.root.geometry('350x450')
        self.root.configure(bg='#314252')
        self.create_widgets()

    def create_widgets(self):
        # Label NIF
        self.nif_entry = tk.Entry(self.root, width=30)
        self.nif_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.root, text='NIF:', fg="white", font=(8), bg='#314252').grid(row=0, column=0, padx=10, pady=5, sticky="e")

        # Label NAME
        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self.root, text='Nombre', fg="white", font=(8), bg='#314252').grid(row=1, column=0, padx=10, pady=5, sticky="e")

        # Label SURNAMES
        self.surnames_entry = tk.Entry(self.root, width=30)
        self.surnames_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(self.root, text='Apellidos:', fg="white", font=(8), bg='#314252').grid(row=2, column=0, padx=10, pady=5, sticky="e")

        # Label ADDRESS
        self.address_entry = tk.Entry(self.root, width=30)
        self.address_entry.grid(row=3, column=1, padx=10, pady=5)
        tk.Label(self.root, text='Domicilio:', fg="white", font=(8), bg='#314252').grid(row=3, column=0, padx=10, pady=5, sticky="e")

        # Label PHONE
        self.phone_entry = tk.Entry(self.root, width=30)
        self.phone_entry.grid(row=4, column=1, padx=10, pady=5)
        tk.Label(self.root, text='Teléfono:', fg="white", font=(8), bg='#314252').grid(row=4, column=0, padx=10, pady=5, sticky="e")

        # Buttons
        tk.Button(self.root, text='Alta usuario', command=self.add_user).grid(row=5, column=0, columnspan=2, padx=10,
                                                                              pady=5)
        tk.Button(self.root, text='Modificar usuario', command=self.modify_user).grid(row=6, column=0, columnspan=2,
                                                                                      padx=10, pady=5)
        tk.Button(self.root, text='Baja usuario', command=self.remove_user).grid(row=7, column=0, columnspan=2,
                                                                                 padx=10, pady=5)
        tk.Button(self.root, text='Lista de usuarios', command=self.list_users).grid(row=8, column=0, columnspan=2,
                                                                                     padx=10, pady=5)
        tk.Label(self.root, text='', bg='#314252').grid(row=9, column=0, pady=5)  # insert some space between the othes buttons
        tk.Button(self.root, text='Salir', command=self.close).grid(row=10, column=0, columnspan=2, pady=5)

    def nif_format(self, nif):
        if len(nif) != 9:
            return False

        letters = ['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H',
                   'L', 'C', 'K', 'E']
        letter = nif[-1].upper()
        numNif = int(nif[:-1])
        module = numNif % 23

        return letter == letters[module]

    # check if NIF format is correct or not
    def validate_nif(self, nif):
        if not self.nif_format(nif) or not nif[:-1].isdigit() or not nif[-1].isalpha(): # check if nif has 9 positions, the first 8 are numbers and if last one is char
            messagebox.showerror('Error', 'El valor introducido no se corresponde con un NIF válido')
            return False
        return True

    # add user DB
    def add_user(self):
        nif = self.nif_entry.get().strip().upper()
        name = self.name_entry.get().strip().title()
        surnames = self.surnames_entry.get().strip().title()
        address = self.address_entry.get().strip().title()
        phone = self.phone_entry.get().strip()

        if not self.validate_nif(nif) or not phone.isdigit():
            return

        query = "INSERT INTO users(nif, name, surnames, address, phone) VALUES (%s, %s, %s, %s, %s)"
        values = nif, name, surnames, address, phone

        try:
            self.db_manager.cursor.execute(query, values)
            self.db_manager.connection.commit()
            messagebox.showinfo('Éxito', 'Usuario dado de alta correctamente.')
        except pymysql.Error as e:
            messagebox.showerror('Error', f'No se ha podido dar de alta el usuario: {e}')

    # remove user DB
    def remove_user(self):
        nif = self.nif_entry.get().strip().upper()

        if not self.validate_nif(nif):
            return

        query = "DELETE from users where nif = %s"

        try:
            self.db_manager.cursor.execute(query, (nif,))
            self.db_manager.connection.commit()
            if self.db_manager.cursor.rowcount > 0: #check if transaction is done
                messagebox.showinfo('Éxito', 'Usuario eliminado correctamente.')
            else:
                messagebox.showerror('Error', 'No se ha encontrado ningún usuario con este NIF.')
        except pymysql.Error as e:
            messagebox.showerror('Error', f'No se ha podido eliminar el usuario: {e}')

    # modify user DB
    def modify_user(self):
        nif = self.nif_entry.get().strip().upper()
        name = self.name_entry.get().strip().title()
        surnames = self.surnames_entry.get().strip().title()
        address = self.address_entry.get().strip().title()
        phone = self.phone_entry.get().strip()

        if not self.validate_nif(nif):
            return

        values = []
        update_fields = []

        if name:
            values.append(name)
            update_fields.append("name = %s")
        if surnames:
            values.append(surnames)
            update_fields.append("surnames = %s")
        if address:
            values.append(address)
            update_fields.append("address = %s")
        if phone:
            values.append(phone)
            update_fields.append("phone = %s")

        query = f"UPDATE users SET {', '.join(update_fields)} WHERE nif = %s"
        values.append(nif)

        try:
            self.db_manager.cursor.execute(query, tuple(values))
            self.db_manager.connection.commit()
            if self.db_manager.cursor.rowcount > 0:
                messagebox.showinfo('Éxito', 'Usuario modificado correctamente.')
            else:
                messagebox.showerror('Error', 'No se ha encontrado ningún usuario con este NIF.')
        except pymysql.Error as e:
            messagebox.showerror('Error', f'No se ha podido modificar el usuario: {e}')

    # a list of users in DB
    def list_users(self):
        query = "SELECT * from users"

        try:
            self.db_manager.cursor.execute(query)
            users = self.db_manager.cursor.fetchall()
            if users:
                user_list = "\n".join(
                    [f"NIF: {user[0]}, Nombre: {user[1]}, Apellidos: {user[2]}, Domicilio: {user[3]}, Teléfono: {user[4]}"
                     for user in users])
                print(user_list)
                messagebox.showinfo('Lista de usuarios', user_list)
                file = messagebox.askokcancel("Guardar lista de usuarios",
                                              "¿Desea guardar la lista de usuarios en un archivo?")
                if file == True:
                    result = filedialog.asksaveasfile(title="Guardar un fichero", mode="w")
                    if result is not None:
                        result.write(user_list)
                        result.close()
            else:
                messagebox.showinfo('Lista de usuarios', 'No hay usuarios dados de alta.')
        except pymysql.Error as e:
            messagebox.showerror('Error', f'No se ha podido mostrar la lista de usuarios: {e}')

    def close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


##Here ends Class USERS##

##Here starts Class BOOKS##
class Books():
    def __init__(self, root, db_manager):
        self.db_manager = db_manager
        self.root = tk.Tk()
        self.root.title('Gestión de libros')
        self.root.geometry('520x450')
        self.root.configure(bg='#314252')
        self.create_widgets()

    def create_widgets(self):
        # Label ID
        self.book_id_entry = tk.Entry(self.root, width=50)
        self.book_id_entry.insert(0, "Rellenar sólo para eliminar o modificar libro")
        self.book_id_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.root, text='ID del libro:', fg="white", font=(8), bg='#314252').grid(row=0, column=0, padx=10, pady=5, sticky="e")

        # Label TITULO
        self.title_entry = tk.Entry(self.root, width=50)
        self.title_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self.root, text='Título del libro', fg="white", font=(8),bg='#314252').grid(row=1, column=0, padx=10, pady=5, sticky="e")

        # Label AUTHOR
        self.author_entry = tk.Entry(self.root, width=50)
        self.author_entry.grid(row=2, column=1, padx=10, pady=5)
        tk.Label(self.root, text='Autor del libro:', fg="white", font=(8), bg='#314252').grid(row=2, column=0, padx=10, pady=5, sticky="e")

        # Label YEAR
        self.year_entry = tk.Entry(self.root, width=50)
        self.year_entry.grid(row=3, column=1, padx=10, pady=5)
        tk.Label(self.root, text='Año del libro:', fg="white", font=(8), bg='#314252').grid(row=3, column=0, padx=10, pady=5, sticky="e")

        # Label STOCK
        self.stock_entry = tk.Entry(self.root, width=50)
        self.stock_entry.grid(row=4, column=1, padx=10, pady=5)
        tk.Label(self.root, text='Stock total:', fg="white", font=(8), bg='#314252').grid(row=4, column=0, padx=10, pady=5, sticky="e")

        # Label AVAILABILITY
        self.availability_entry = tk.Entry(self.root, width=50)
        self.availability_entry.grid(row=5, column=1, padx=10, pady=5)
        tk.Label(self.root, text='Ejemplares disponibles:', fg="white", font=(8), bg='#314252').grid(row=5, column=0, padx=10, pady=5, sticky="e")

        # Buttons
        tk.Button(self.root, text='Alta nuevo libro', command=self.add_book).grid(row=6, column=0, columnspan=2,
                                                                                  padx=10, pady=5)
        tk.Button(self.root, text='Modificar libro', command=self.modify_book).grid(row=7, column=0, columnspan=2,
                                                                                    padx=10, pady=5)
        tk.Button(self.root, text='Baja libro', command=self.remove_book).grid(row=8, column=0, columnspan=2, padx=10,
                                                                               pady=5)
        tk.Button(self.root, text='Lista de libros', command=self.list_books).grid(row=9, column=0, columnspan=2,
                                                                                   padx=10, pady=5)
        tk.Label(self.root, text='', bg="#314252").grid(row=10, column=0, pady=5)  # insert some space between the othes buttons
        tk.Button(self.root, text='Salir', command=self.close).grid(row=11, column=0, columnspan=2, pady=5)

    def validate_book_id(self, book_id):
        if not book_id or not book_id.isdigit(): #check if we´ve got a bokk_id or the  book_id has chars
            messagebox.showerror('Error', 'El ID del libro debe ser un número entero.')
            return False
        return True

    def validate_author_name(self, author_name):
        for char in author_name:
            if char.isdigit(): #check if we´ve got a name or the name has numbers
                messagebox.showerror('Error', 'El nombre del autor está vacio o no tine el '
                                              'formato correcto.')
                return False
        return True

    # add new book
    def add_book(self):
        # book_id = self.book_id_entry.get().strip()
        title = self.title_entry.get().strip().title()
        author_name = self.author_entry.get().strip().title()
        year = self.year_entry.get().strip()
        stock = self.stock_entry.get().strip()
        availability = self.availability_entry.get().strip()

        if not self.validate_author_name(author_name):
            return

        query = "INSERT INTO books (title, author, year, stock, availability) VALUES (%s, %s, %s, %s, %s)"
        values = title, author_name, year, stock, availability

        try:
            self.db_manager.cursor.execute(query, values)
            self.db_manager.connection.commit()
            messagebox.showinfo('Éxito', 'Libro dado de alta correctamente.')
        except pymysql.Error as e:
            messagebox.showerror('Error', f'No se ha podido dar de alta el libro: {e}')

    # edit a book
    def modify_book(self):
        book_id = self.book_id_entry.get().strip()
        title = self.title_entry.get().strip().title()
        if not title:  # validate if we have or not a title
            title = None
        author_name = self.author_entry.get().strip().title()
        if not author_name:
            author_name = None
        year = self.year_entry.get().strip()
        if year:
            year = int(year)  # if we have a year transform to integer
        else:
            year = None
        stock = self.stock_entry.get().strip()
        if stock:
            stock = int(stock)  # if we have stock transform to integer
        else:
            stock = None
        availability = self.availability_entry.get().strip()
        if availability:
            availability = int(availability)  # if we have availability transform to integer
        else:
            availability = None

        # Verifica book_id y si author_name es no None
        if not self.validate_book_id(book_id) or (
                author_name is not None and not self.validate_author_name(author_name)):
            return

        values = []
        update_fields = []

        if title:
            values.append(title)
            update_fields.append("title = %s")
        if author_name:
            values.append(author_name)
            update_fields.append("author = %s")
        if year:
            values.append(year)
            update_fields.append("year = %s")
        if stock:
            values.append(stock)
            update_fields.append("stock = %s")
        if availability:
            values.append(availability)
            update_fields.append("availability = %s")

        query = f"UPDATE books SET {', '.join(update_fields)} WHERE book_id = %s"
        values.append(book_id)

        try:
            self.db_manager.cursor.execute(query, tuple(values))
            self.db_manager.connection.commit()

            if self.db_manager.cursor.rowcount > 0:  # check if transaction is done
                messagebox.showinfo('Éxito', 'Libro modificado correctamente.')
            else:
                messagebox.showerror('Error', 'No se ha encontrado ningún libro con ese ID.')
        except pymysql.Error as e:
            messagebox.showerror('Error', f'No se ha podido modificar el libro: {e}')

    # remove a book from the list
    def remove_book(self):
        book_id = self.book_id_entry.get().strip()

        if not self.validate_book_id(book_id):
            return

        query = "DELETE from books WHERE book_id = %s"
        try:
            self.db_manager.cursor.execute(query, (book_id,))
            self.db_manager.connection.commit()
            if self.db_manager.cursor.rowcount > 0: #check if transaction is done
                messagebox.showinfo('Éxito', 'Libro eliminado correctamente.')
            else:
                messagebox.showerror('Error', 'No se ha encontrado ningún libro con ese ID.')
        except pymysql.Error as e:
            messagebox.showerror('Error', f'No se ha podido eliminar el libro: {e}')

    # list all the books
    def list_books(self):
        query = "SELECT * from books"

        try:
            self.db_manager.cursor.execute(query)
            books = self.db_manager.cursor.fetchall()
            if books:
                book_list = "\n".join(f'ID del libro: {book[0]}, Título: {book[1]}, Autor del libro: {book[2]},'
                                      f' Año del libro: {book[3]}, Stock total: {book[4]}, Ejemplares disponibles: '
                                      f'{book[5]}' for book in books)
                messagebox.showinfo('Catálogo de libros', book_list)
                file = messagebox.askokcancel("Guardar lista de libros",
                                              "¿Desea guardar la lista de libros en un archivo?")
                if file == True:
                    result = filedialog.asksaveasfile(title="Guardar un fichero", mode="w", filetypes=(("Fichero de texto", "*.txt"),))
                    if result is not None:
                        result.write(book_list)
                        result.close()
            else:
                messagebox.showinfo('Catálogo de libros', 'No hay libros en la biblioteca.')
        except pymysql.Error as e:
            messagebox.showerror('Error', f'No se ha podido obtener la lista de libros: {e}')

    def close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

##Here ends Class BOOK##

##Here starts Class LOAN##
class Loans():
    def __init__(self, root, db_manager):
        self.root = tk.Tk()
        self.db_manager = db_manager
        self.root.title('Gestión de préstamos')
        self.root.geometry('350x300')
        self.root.configure(bg="#314252")
        self.create_widgets()

    def create_widgets(self):
        # Label NIF
        self.nif_entry = tk.Entry(self.root, width=30)
        self.nif_entry.grid(row=0, column=1, padx=10, pady=5)
        tk.Label(self.root, text='NIF:', bg="#314252", fg="white", font=8).grid(row=0, column=0, padx=10, pady=5)

        # Label BOOK_ID
        self.book_id_entry = tk.Entry(self.root, width=30)
        self.book_id_entry.grid(row=1, column=1, padx=10, pady=5)
        tk.Label(self.root, text='ID del libro:', bg="#314252", fg="white", font=8).grid(row=1, column=0, padx=10,
                                                                                           pady=5)
        # buttons
        tk.Button(self.root, text='Prestar libro', command=self.loan_book).grid(row=2, column=0, columnspan=2,
                                                                                pady=5)
        tk.Button(self.root, text='Devolver libro', command=self.return_book).grid(row=3, column=0, columnspan=2,
                                                                                   pady=5)
        tk.Button(self.root, text='Mostrar préstamos', command=self.list_loans).grid(row=4, column=0, columnspan=2,
                                                                                     pady=5)
        tk.Label(self.root, text='', bg="#314252").grid(row=5, column=0, pady=5) # insert some space between the othes buttons
        tk.Button(self.root, text='Salir', command=self.close).grid(row=6, column=0, columnspan=2, pady=5)

    def nif_format(self, nif):
        if len(nif) != 9:
            return False

        letters = ['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H',
                   'L', 'C', 'K', 'E']
        letter = nif[-1].upper()
        numNif = int(nif[:-1])
        module = numNif % 23

        if letter == letters[module]:
            return True
        else:
            return False

    # check if NIF format is correct or not
    def validate_nif(self, nif):
        if not self.nif_format(nif) or not nif[:-1].isdigit() or not nif[-1].isalpha():  # check if nif has 9
            # positions, the first 8 are numbers and if last one is char
            messagebox.showerror('Error', 'El valor introducido no se corresponde con un NIF válido')
            return False
        return True

    # check if BOOK_ID has the right format
    def validate_book_id(self, book_id):
        if not book_id or not book_id.isdigit():
            messagebox.showerror('Error', 'El ID del libro debe ser un número entero.')
            return False
        return True

    # loan a BOOK
    def loan_book(self):

        nif = self.nif_entry.get().strip().upper()
        book_id = self.book_id_entry.get().strip()

        if not self.validate_nif(nif) or not self.validate_book_id(book_id):
            return
        query_select = "SELECT availability FROM books WHERE book_id = %s"
        query_insert = "INSERT INTO loans (nif, book_id) values(%s, %s)"
        query_update = "UPDATE books SET availability = availability - 1 WHERE book_id = %s"
        values = nif, book_id
        try:
            #we check avilability of the book for loan
            self.db_manager.cursor.execute(query_select, (book_id,))
            availability = self.db_manager.cursor.fetchone()[0] # we show only one line
            if availability <= 0:
                messagebox.showerror('Error', 'No hay ejemplares disponibles.')
                return
            #we insert book if availability
            self.db_manager.cursor.execute(query_insert, (nif, book_id))
            self.db_manager.cursor.execute(query_update, (book_id,))
            self.db_manager.connection.commit()
            messagebox.showinfo("Éxito", "Libro prestado correctamente.")
        except Exception as e:
            messagebox.showerror('Error', f'Error al prestar el libro: {e}')
            self.db_manager.connection.rollback() #if transaction is not complete we restart db as before"""

    # return a BOOK
    def return_book(self):
        nif = self.nif_entry.get().strip().upper()
        book_id = self.book_id_entry.get().strip()

        if not self.validate_nif(nif) or not self.validate_book_id(book_id):
            return

        query_delete = "DELETE from loans WHERE nif = %s AND book_id = %s"
        query_update = "UPDATE books SET availability = availability + 1 WHERE book_id = %s"
        values = nif, book_id

        try:
            self.db_manager.cursor.execute(query_delete, values)
            if self.db_manager.cursor.rowcount == 0: #we check if transaction is done, if not show message
                messagebox.showerror('Error', 'No se ha encontrado ningún préstamo con este NIF o ID de libro.')
                return

            self.db_manager.cursor.execute(query_update, (book_id,))
            self.db_manager.connection.commit()
            messagebox.showinfo('Éxito', 'Libro devuelto correctamente.')
        except pymysql.Error as e:
            messagebox.showerror('Error', f'No se ha devuelto ningún libro: {e}')
            self.db_manager.connection.rollback() #if transaction is not complete we restart db as before

    # list all the loans
    def list_loans(self):
        query = "SELECT * from loans"
        try:
            self.db_manager.cursor.execute(query)
            loans = self.db_manager.cursor.fetchall()

            if loans:
                loan_list = "\n".join(f'NIF: {loan[0]}, ID del libro: {loan[1]}' for loan in loans)
                messagebox.showinfo('Préstamos realizados', loan_list)
            else:
                messagebox.showinfo('Préstamos realizados', 'No se ha prestado ningún libro.')
        except pymysql.Error as e:
            messagebox.showerror('Error', f'No se ha obtenido la lista de préstamos: {e}')

    def close(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()


##here ends Class LOAN##

##here starts Class MENU##
class Menu():
    def __init__(self, db_manager):
        self.root = tk.Tk()
        self.db_manager = db_manager
        self.root.title('Biblioteca')
        self.root.geometry('1000x650')
        #self.root.configure(bg='lightyellow')
        self.create_widgets()

    def create_widgets(self):
        # Menu
        menubar = tk.Menu(self.root)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Gestión de Usuarios", command=self.manage_users)
        filemenu.add_separator()
        filemenu.add_command(label="Gestión de Libros", command=self.manage_books)
        filemenu.add_separator()
        filemenu.add_command(label="Gestión de Préstamos", command=self.manage_loans)
        menubar.add_cascade(menu=filemenu, label="Gestionar")

        exitmenu = tk.Menu(menubar, tearoff=0)
        exitmenu.add_command(label="Salir", command=self.close)
        menubar.add_cascade(menu=exitmenu, label="Salir")

        self.root.config(menu=menubar)

        # Frame
        frame = Frame(self.root)
        frame.pack(fill="both", expand=1)
        frame.configure(padx=10, pady=5, bg="#314252")

        # labels
        """photo = PhotoImage(file="libro.gif")

        image_label = Label(frame, image=photo, bd=0, padx=40)
        image_label.image = photo
        image_label.pack(side="left")"""

        text_label = Label(frame, text="Bienvenido al sistema \nde gestión de la Biblioteca.",
                           font=("Consolas", 34), padx=24, pady=10, bg="#314252", fg="white")
        text_label.pack(anchor="center")

    def manage_users(self):
        usersGUI = Users(self.root, self.db_manager)
        usersGUI.run()

    def manage_books(self):
        booksGUI = Books(self.root, self.db_manager)
        booksGUI.run()

    def manage_loans(self):
        loansGUI = Loans(self.root, self.db_manager)
        loansGUI.run()

    def run(self):
        self.root.mainloop()

    def close(self):
        self.db_manager.close()
        self.root.quit()


if __name__ == "__main__":
    db_manager = DataBaseManager()
    menuGUI = Menu(db_manager)
    menuGUI.run()
##here ends Class MENU##