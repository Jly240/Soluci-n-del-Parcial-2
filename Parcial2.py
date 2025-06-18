import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, db

# ---------------- CONFIGURAR FIREBASE ---------------- #

# Cargar credenciales desde el archivo .json
cred = credentials.Certificate("BaseDeDatos.json")          #Rellenar con el Nuevo JSON
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://parcial2-c2b14-default-rtdb.firebaseio.com/"     #Reemplazar por el link del proyecto
})

# ---------------- CLASES ---------------- #

class Libro:
    def __init__(self, titulo, autor, categoria):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria

    def to_dict(self):
        return {
            "titulo": self.titulo,   #Aqui nor encargamos de definir lo que va a defirencicar cada libro
            "autor": self.autor,
            "categoria": self.categoria
        }

class Usuario:
    def __init__(self, nombre, correo):
        self.nombre = nombre             #Y aqui vamos a definir la información que van a introducir los estudintes
        self.correo = correo

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "correo": self.correo
        }

# ---------------- FUNCIONES UI ---------------- #

def registrar_libro():
    def guardar():
        titulo = entrada_titulo.get()
        autor = entrada_autor.get()
        categoria = categoria_var.get()     #Definimos la funcion de las cajas de texto en el regristro de los libros
        if titulo and autor:
            libro = Libro(titulo, autor, categoria)
            db.reference("libros").push(libro.to_dict())
            messagebox.showinfo("Éxito", "Libro registrado en Firebase.")
            ventana.destroy()
        else:
            messagebox.showerror("Error", "Completa todos los campos.")

    ventana = tk.Toplevel()
    ventana.title("Registro de Libros")
    ventana.geometry("400x300")  # Tamaño más grande para la ventana

    tk.Label(ventana, text="Título del libro:").pack(pady=5)
    entrada_titulo = tk.Entry(ventana, font=("Arial", 12))
    entrada_titulo.pack(pady=5)

    tk.Label(ventana, text="Autor:").pack(pady=5)
    entrada_autor = tk.Entry(ventana, font=("Arial", 12))
    entrada_autor.pack(pady=5)

    tk.Label(ventana, text="Categoría:").pack(pady=5)
    categoria_var = tk.StringVar(ventana)
    categoria_var.set(categorias[0])
    tk.OptionMenu(ventana, categoria_var, *categorias).pack(pady=5)   #Tambien nos encargamos de definir el color y l fuente que se usara en los botones

    tk.Button(ventana, text="Guardar", command=guardar, bg="#87CEEB", fg="white", font=("Arial", 14, "bold"), width=20, height=2).pack(pady=10)

def registrar_usuario():
    def guardar():
        nombre = entrada_nombre.get()
        correo = entrada_correo.get()       #Y tambien definimos las cajas de texto en donde el ususario introdicirá la informacion que se subiráa la base de datos
        if nombre and correo:
            usuario = Usuario(nombre, correo)
            db.reference("usuarios").push(usuario.to_dict())
            messagebox.showinfo("Éxito", "Usuario registrado en Firebase.")
            ventana.destroy()
        else:
            messagebox.showerror("Error", "Completa todos los campos.")

    ventana = tk.Toplevel()        #Por acá ponemos el título de la ventana y el tamaño respectivamente"
    ventana.title("Registrar Usuario")
    ventana.geometry("400x300")  # Tamaño más grande para la ventana

    tk.Label(ventana, text="Nombre:").pack(pady=5)
    entrada_nombre = tk.Entry(ventana, font=("Arial", 12))
    entrada_nombre.pack(pady=5)

    tk.Label(ventana, text="Correo:").pack(pady=5)
    entrada_correo = tk.Entry(ventana, font=("Arial", 12))
    entrada_correo.pack(pady=5)                              #Tabien defnimos Los colores y dimensione del botón

    tk.Button(ventana, text="Guardar", command=guardar, bg="#87CEEB", fg="white", font=("Arial", 14, "bold"), width=20, height=2).pack(pady=10)

def buscar_libro():
    def buscar():
        query = entrada_busqueda.get().lower()
        lista_resultados.delete(0, tk.END)
        libros_firebase = db.reference("libros").get()   #Acá definimos como el programa va a buscar los libros en la base de datos
        if libros_firebase:
            for datos in libros_firebase.values():
                if query in datos["titulo"].lower():
                    lista_resultados.insert(tk.END, f'{datos["titulo"]} - {datos["autor"]} [{datos["categoria"]}]')
        else:
            lista_resultados.insert(tk.END, "No hay libros registrados.")

    ventana = tk.Toplevel()
    ventana.title("Buscar Libro")
    ventana.geometry("400x300")  

    tk.Label(ventana, text="Buscar por título:").pack(pady=5)
    entrada_busqueda = tk.Entry(ventana, font=("Arial", 12))
    entrada_busqueda.pack(pady=5)

    tk.Button(ventana, text="Buscar", command=buscar, bg="#87CEEB", fg="white", font=("Arial", 14, "bold"), width=20, height=2).pack(pady=10)

    lista_resultados = tk.Listbox(ventana, width=50, height=10)
    lista_resultados.pack(pady=10)

# ---------------- INTERFAZ PRINCIPAL ---------------- #

categorias = ["Ciencia", "Literatura", "Matemáticas"]

root = tk.Tk()
root.title("Biblioteca Universitaria")
root.geometry("400x400")

# Título en azul oscuro y fuente llamativa
titulo = tk.Label(root, text="Simulador Biblioteca", font=("Helvetica", 18, "bold"), fg="#003366") #Por aca se define la fuente, el tamaño y el color del titulo
titulo.pack(pady=20)

# Definición de medidas colores y fuentes de los botones de la pagina rincipal
tk.Button(root, text="Registrar Libro", width=30, command=registrar_libro, bg="#87CEEB", fg="white", font=("Arial", 14, "bold"), height=2).pack(pady=10)
tk.Button(root, text="Registrar Usuario", width=30, command=registrar_usuario, bg="#87CEEB", fg="white", font=("Arial", 14, "bold"), height=2).pack(pady=10)
tk.Button(root, text="Buscar Libro", width=30, command=buscar_libro, bg="#87CEEB", fg="white", font=("Arial", 14, "bold"), height=2).pack(pady=10)

# Pie de página
tk.Label(root, text="Desarrollado por: Julian Rodriguez", font=("Arial", 10)).pack(side="bottom", pady=10)

root.mainloop()

