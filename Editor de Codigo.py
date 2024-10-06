import tkinter as tk
from tkinter import filedialog, messagebox
import pyperclip

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

# Menú Editar
menu_editar = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Editar", menu=menu_editar)
def Pegar():
    pyperclip.paste()
    
def Cortar():
    pyperclip.cut() 
        
def Copiar():
    pyperclip.copy()   

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
