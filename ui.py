import database as db
import helpers
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING

class CenterWidgetMixin:
        def center(self):
            self.update()
            w = self.winfo_width()
            h = self.winfo_height()
            ws = self.winfo_screenwidth()
            hs = self.winfo_screenheight()
            x = int(ws/2 - w/2)
            y = int(hs/2 - h/2)
            self.geometry(f"{w}x{h}+{x}+{y}")#WIDTHxHEIGHT+OFFSET_X+OFFSET_Y
    
class CreatClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Crear Cliente")
        self.build()
        self.center()
        # Estos dos me obligan a realizar una accion con la ventana emergente
        self.transient(parent)
        self.grab_set()
        
    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)
        
        
        Label(frame, text="DNI (2 ints y 1 upper char)").grid(row=0, column=0)
        Label(frame, text="Nombre (de 2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (de 2 a 30 chars)").grid(row=0, column=2)
        
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        dni.bind("<KeyRelease>", lambda event: self.validate(event,0))
        
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event,1))
        
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 2))
        
        frame = Frame(self)
        frame.pack(pady=10)
        
        crear = Button(frame, text="Crear", command=self.creat_client)
        crear.config(state=DISABLED)
        crear.grid(row=0, column=0, padx=10)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1, padx=10)
        
        self.validaciones = [False,False,False]
        self.crear = crear
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        

            
    def creat_client(self):
            self.master.treeview.insert(
                parent="", index="end", iid=self.dni.get(), 
                values=(self.dni.get(), self.nombre.get(), self.apellido.get()))
            db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get())
            self.close()
    
    def close(self):
        self.destroy()
        self.update()
        
    def validate(self, event, index):
        valor = event.widget.get()
        if index == 0:
            valido = helpers.dni_valido(valor, db.Clientes.lista)
            if valido:
                event.widget.configure({"bg":"Green"})
            else:
                event.widget.configure({"bg":"Red"})
        elif index == 1:
            valido = len(valor) >= 2 and len(valor) <= 30
            if valido:
                event.widget.configure({"bg":"Green"})
            else:
                event.widget.configure({"bg":"Red"})
        elif index == 2:
            valido = len(valor) >= 2 and len(valor) <= 30
            if valido:
                event.widget.configure({"bg":"Green"})
            else:
                event.widget.configure({"bg":"Red"})
        # Otra manera de hacerlo puede ser asi:
        #valor = event.widget.get()
        #valido = helpers.dni_valido(valor, db.Clientes.lista) if index==0
                #else (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30)
            #event.widget.configure({"bg": "Gree" if valido else "Red"})
        ### Cambiar el estado del boton segun las validaciones:
        self.validaciones[index] = valido
        self.crear.config(state=NORMAL if self.validaciones == [True, True, True] else DISABLED)

class EditClientWindow(Toplevel, CenterWidgetMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Actualizar Cliente")
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()
        
    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)
        
        Label(frame, text="DNI (No Editable.)").grid(row=0, column=0)
        Label(frame, text="Nombre (de 2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (de 2 a 30 chars)").grid(row=0, column=2)
        
        dni = Entry(frame)
        dni.grid(row=1, column=0)
        nombre = Entry(frame)
        nombre.grid(row=1, column=1)  
        nombre.bind("<KeyRelease>", lambda event: self.validate(event,0))
        apellido = Entry(frame)
        apellido.grid(row=1, column=2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event,1))
        
        cliente = self.master.treeview.focus()
        campos = self.master.treeview.item(cliente, "values")
        dni.insert(0, campos[0])
        dni.config(state=DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])
        
        
        frame = Frame(self)
        frame.pack(pady=10)
        
        actualizar = Button(frame, text="Actualizar", command=self.update_client)
        actualizar.grid(row=0, column=0)
        Button(frame, text="Cancelar", command=self.close).grid(row=0, column=1)
        
        self.validaciones = [1,1]
        self.actualizar = actualizar
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido    
    
    def validate(self, event, index):
        valor = event.widget.get()
        if index == 0:
            valido =  len(valor) >= 2 and len(valor) <= 30
            if valido:
                event.widget.configure({"bg":"Green"})
            else:
                event.widget.configure({"bg":"Red"})
        elif index == 1:
            valido =  len(valor) >= 2 and len(valor) <= 30
            if valido:
                event.widget.configure({"bg":"Green"})
            else:
                event.widget.configure({"bg":"Red"})
    
        self.validaciones[index] =valido
        self.actualizar.config(state=NORMAL if self.validaciones == [1,1] else DISABLED)
        
    def update_client(self):
        cliente = self.master.treeview.focus()
        self.master.treeview.item(cliente, values=(self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()
        
    def close(self):
        self.destroy()
        self.update()               
        
class MainWindow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Clientes")
        self.build()
        self.center()
        self.delete()
        
    def build(self):
        frame = Frame(self)
        frame.pack(pady=20)
        
        Label(frame, text="Search").grid(row=0, column=0)
        name_to_search = Entry(frame)
        name_to_search.grid(row=0, column=1)
        name_to_search.bind("<KeyRelease>", self.update_search_results)
        
        self.name_to_search= name_to_search
        
        #apellido.bind("<KeyRelease>", lambda event: self.validate(event, 2))
        
        
        frame = Frame(self)
        frame.pack()
        
        
        treeview = ttk.Treeview(frame)
        treeview["columns"] = ("DNI", "Nombre", "Apellido")
        
        treeview.column("#0", width=0, stretch=NO)
        treeview.column("DNI", anchor=CENTER)
        treeview.column("Nombre", anchor=CENTER)
        treeview.column("Apellido", anchor=CENTER)
        
        treeview.heading("DNI", text="DNI", anchor=CENTER)
        treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        treeview.heading("Apellido", text="Apellido", anchor=CENTER)
        
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        treeview["yscrollcommand"] = scrollbar.set
        
        for cliente in db.Clientes.lista:
            treeview.insert(
                parent="", index="end", iid=cliente.dni, 
                values=(cliente.dni, cliente.nombre, cliente.apellido)
            )
        
        treeview.pack()

        
        frame = Frame(self)
        frame.pack(pady=20)

        
        Button(frame, text="Crear", command=self.create).grid(row=0, column=0, padx=10)
        Button(frame, text="modificar", command=self.edit).grid(row=0, column=1, padx=10)
        Button(frame, text="Borrar", command=self.delete).grid(row=0, column=2, padx=10)

        self.treeview = treeview
        
    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente, "values") # de esta manera se pueden extraer los valores que hayan en la tabla segun se haya seleccionado
            confirmar = askokcancel(
                title = "Confirmar Borrado",
                message = f"Borrar el Usuario {campos[1]} {campos[2]}",
                icon = WARNING
            )
            if confirmar :
                self.treeview.delete(cliente)
                db.Clientes.borrar(campos[0])
        
       

    def create(self):
        CreatClientWindow(self)
    
    def edit(self):
        if self.treeview.focus():
            EditClientWindow(self)
            
    def update_search_results(self, event):
        search_term = self.name_to_search.get().lower()
        
        if len(search_term) < 0:
            for cliente in db.Clientes.lista:
                self.treeview.insert(
                    parent="", index="end", iid=cliente.dni, 
                    values=(cliente.dni, cliente.nombre, cliente.apellido)
                )
        
        self.treeview.delete(*self.treeview.get_children())
        
        for cliente in db.Clientes.lista:
            if search_term in cliente.nombre.lower():
                self.treeview.insert(
                    parent="", index="end", iid=cliente.dni,
                    values=(cliente.dni, cliente.nombre, cliente.apellido)
                )
    
        

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()