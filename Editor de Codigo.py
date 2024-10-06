import tkinter as tk
from tkinter import filedialog, messagebox
import pyperclip
import os

# Crear la ventana principal
root = tk.Tk()
root.title("Bloc de Notas")
root.geometry("600x400")

# Funciones para las opciones de menú

# Crear el área de texto
text_area = tk.Text(root, undo=True)
text_area.pack(fill=tk.BOTH, expand=True)

# Crear la barra de menú
menu_bar = tk.Menu(root)

# Menú Archivo
menu_archivo = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Archivo", menu=menu_archivo)
archivos_recientes = []

def nuevo_archivo():
    nombre_archivo = input("Ingresa el nombre del nuevo archivo (con extensión): ")
    open(nombre_archivo, 'w').close()
    print(f"Archivo '{nombre_archivo}' creado exitosamente.")
    agregar_a_archivos_recientes(nombre_archivo)

def abrir_archivo():
    nombre_archivo = input("Ingresa el nombre del archivo a abrir (con extensión): ")
    if os.path.isfile(nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            print(f"Contenido del archivo '{nombre_archivo}':\n{archivo.read()}")
        agregar_a_archivos_recientes(nombre_archivo)
    else:
        print(f"El archivo '{nombre_archivo}' no existe.")

def guardar_archivo(nombre_archivo, contenido):
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(contenido)
    print(f"Archivo '{nombre_archivo}' guardado exitosamente.")
    agregar_a_archivos_recientes(nombre_archivo)

def guardar_como():
    nuevo_nombre_archivo = input("Ingresa el nombre para guardar el archivo (con extensión): ")
    contenido = input("Ingresa el contenido que deseas guardar: ")
    guardar_archivo(nuevo_nombre_archivo, contenido)

def imprimir_archivo(nombre_archivo):
    if os.path.isfile(nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            print(f"Contenido del archivo '{nombre_archivo}':\n{archivo.read()}")
    else:
        print(f"El archivo '{nombre_archivo}' no existe.")

def salir():
    print("Saliendo del programa...")
    exit()

def agregar_a_archivos_recientes(nombre_archivo):
    if nombre_archivo not in archivos_recientes:
        archivos_recientes.append(nombre_archivo)
    else:
        archivos_recientes.remove(nombre_archivo)
        archivos_recientes.append(nombre_archivo)
    
    if len(archivos_recientes) > 5:
        archivos_recientes.pop(0)

def mostrar_archivos_recientes():
    print("\nArchivos recientes:")
    for archivo in archivos_recientes:
        print(f"- {archivo}")

# Menú Editar
menu_editar = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Editar", menu=menu_editar)
def Pegar():
    pyperclip.paste()
    
def Cortar():
    pyperclip.cut() 
        
def Copiar():
    pyperclip.copy()   

def Deshacer():
    pyperclip.undo()
 
def Rehacer():
    pyperclip.redo()

# Menú Buscar
menu_buscar = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Buscar", menu=menu_buscar)

# Menú Ver (Opcional para futuras funciones)
menu_ver = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Ver", menu=menu_ver)

# Menú Ejecutar (Opcional para futuras funciones)
menu_ejecutar = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Ejecutar", menu=menu_ejecutar)

# Menú Acerca de
menu_acerca = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Acerca de", menu=menu_acerca)

# Configurar la barra de menú
root.config(menu=menu_bar)

# Iniciar el loop principal de la aplicación
root.mainloop()
