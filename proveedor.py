from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from tkinter import filedialog
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.tables import TableStyle
from tkinter import filedialog
from database import conectar, crear_tablas

class ProveedorApp(Tk):
    def __init__(self, parent):
        super().__init__()
        self.title('Proveedores')
        self.parent = parent  # Almacenar una referencia al objeto PresupuestoApp
        # Resto del código...
        
        crear_tablas()
        self.conn, self.c = conectar()

        def render_proveedores():
            rows = self.c.execute("SELECT * FROM proveedores").fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert('', END, row[0], values=(row[1], row[2], row[3]))

        def insertar(proveedores):
            self.c.execute("""
                    INSERT INTO proveedores (nombre, telefono, direccion) VALUES (?, ?, ?)
                    """, (proveedores['nombre'], proveedores['telefono'], proveedores['direccion']))
            self.conn.commit()
            self.parent.actualizar_nombres_proveedores()
            render_proveedores()

        def nuevo_proveedor():
            def guardar():
                # Validar para no cargar datos vacios
               # if not nombre.get():
                    #messagebox.showerror('Error', 'El nombre es obligatorio')
                    #return
                #if not telefono.get():
                    #messagebox.showerror('Error', 'El telefono es obligatorio')
                   # return

                proveedores = {
                    'nombre': nombre.get(),
                    'telefono': telefono.get(),
                    'direccion': direccion.get()
                }
                insertar(proveedores)
                top.destroy()

            # Definimos una subventana
            top = Toplevel()
            top.title('Nuevo Proveedor')

            lnombre = Label(top, text='Nombre')
            nombre = Entry(top, width=40)
            lnombre.grid(row=0, column=0)
            nombre.grid(row=0, column=1)

            ltelefono = Label(top, text='Telefono')
            telefono = Entry(top, width=40)
            ltelefono.grid(row=1, column=0)
            telefono.grid(row=1, column=1)
            
            ltelefono = Label(top, text='Direccion')
            telefono = Entry(top, width=40)
            ltelefono.grid(row=1, column=0)
            telefono.grid(row=1, column=1)

            guardar = Button(top, text='Guardar', command=guardar)
            guardar.grid(row=3, column=1)

            # Creamos el main loop para nuestra segunda ventana
            top.mainloop()

        def eliminar_proveedor():
            id = self.tree.selection()[0]
            cliente = self.c.execute("SELECT * FROM proveedores where id = ?", (id,)).fetchone()
            respuesta = messagebox.askokcancel('Seguro', 'Estas seguro de querer eliminar el proveedor ' + proveedor[1] + '?')
            if respuesta:
                self.c.execute("DELETE FROM proveedores WHERE id = ?", (id,))
                self.conn.commit()
                render_proveedores()
            else:
                pass

        btn = Button(self, text='Nuevo Proveedor', command=nuevo_proveedor)
        btn.grid(column=0, row=0)

        btn_eliminar = Button(self, text='Eliminar Proveedor', command=eliminar_proveedor)
        btn_eliminar.grid(column=1, row=0)

        self.tree = ttk.Treeview(self)
        self.tree['columns'] = ('Nombre', 'Telefono', 'Direccion')
        self.tree.column('#0', width=0, stretch=NO)
        self.tree.column('Nombre')
        self.tree.column('Telefono')
        self.tree.column('Direccion')

        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Telefono', text='Telefono')
        self.tree.heading('Direccion', text='Direccion')
        self.tree.grid(column=0, row=1, columnspan=4)

        render_proveedores()

if __name__ == '__main__':
    app = ProveedorApp()
    app.mainloop()