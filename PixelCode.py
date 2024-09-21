import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

# Crear la ventana principal
root = tk.Tk()
root.state('zoomed')  # Maximizar la ventana
root.title("PixelCode v0.4")  # Título de la ventana
root.geometry("600x400")  # Tamaño inicial de la ventana

# Centralizar ventana
wtotal = root.winfo_screenwidth()  # Ancho total de la pantalla
htotal = root.winfo_screenheight()  # Alto total de la pantalla

wventana = 600  # Ancho de la ventana
hventana = 400  # Alto de la ventana

# Calcular posición para centrar la ventana
pwidth = round(wtotal / 2 - wventana / 2)
pheight = round(htotal / 2 - hventana / 2)
root.geometry(f"{wventana}x{hventana}+{pwidth}+{pheight}")  # Posicionar la ventana

#-------------------------------------------------------------------------------------------------
def nuevo_archivo():
    """Crea un nuevo archivo en el editor."""
    root.title("Untitled")  # Cambiar el título a 'Sin título'
    text_area.delete(1.0, tk.END)  # Limpiar el área de texto

def abrir_archivo():
    """Abre un archivo de código existente."""
    archivo = filedialog.askopenfilename(defaultextension=".py", 
                                         filetypes=[("Archivos de Código", "*.py")])
    if not archivo:  # Si el usuario cancela la selección
        return

    try:
        root.title(os.path.basename(archivo))  # Cambiar título a nombre del archivo
        text_area.delete(1.0, tk.END)  # Limpiar el área de texto
        with open(archivo, "r") as archivo_abierto:  # Abrir el archivo
            text_area.insert('1.0', archivo_abierto.read())  # Leer y mostrar contenido
    except Exception:
        messagebox.showerror(message="No se puede leer el Archivo!", title="Error")

def guardar_archivo():
    """Guarda el contenido del área de texto en un archivo."""
    archivo = filedialog.asksaveasfilename(defaultextension=".py",
                                           filetypes=[("Archivos de Código", "*.py")])
    if not archivo:  # Si el usuario cancela la selección
        return

    # Verificar si el archivo tiene extensión .py, si no la tiene, agregarla
    if not archivo.endswith(".py"):
        archivo += ".py"

    try:
        # Guarda el contenido del área de texto en el archivo
        with open(archivo, "w") as archivo_guardado:
            contenido = text_area.get(1.0, tk.END)  # Obtener contenido del área de texto
            archivo_guardado.write(contenido)  # Escribir contenido en el archivo

        root.title(os.path.basename(archivo))  # Cambiar el título a nombre del archivo
    except Exception as e:
        messagebox.showerror(message=f"No se puede guardar el archivo: {str(e)}", title="Error")

def cortar_texto():
    """Corta el texto seleccionado en el área de texto."""
    text_area.event_generate("<<Cut>>")

def copiar_texto():
    """Copia el texto seleccionado en el área de texto."""
    text_area.event_generate("<<Copy>>")

def pegar_texto():
    """Pega el texto del portapapeles en el área de texto."""
    text_area.event_generate("<<Paste>>")

def salir():
    """Cierra la aplicación."""
    root.destroy()

# Funciones para aplicar el resaltado de sintaxis
def apply_syntax_highlighting(event=None):
    """Aplica resaltado de sintaxis al código en el área de texto."""
    # Obtener el contenido del área de texto
    text_content = text_area.get("1.0", tk.END)

    # Limpiar todos los tags existentes
    for tag in text_area.tag_names():
        text_area.tag_delete(tag)

    # Obtener el lexer y aplicar resaltado con pygments
    lexer = PythonLexer()  # Puedes cambiar el lexer si usas otro lenguaje
    tokens = lex(text_content, lexer)  # Tokenizar el contenido del texto
    
    # Obtener el esquema de colores del estilo Material
    style = get_style_by_name("material")  # Estilo "material" de Pygments
    
    # Aplicar colores a los tokens
    for token_type, value in tokens:
        start_index = text_area.search(value, "1.0", tk.END)
        while start_index:
            end_index = f"{start_index}+{len(value)}c"
            tag_name = str(token_type)

            # Crear un tag para cada tipo de token si no existe
            if tag_name not in text_area.tag_names():
                token_style = style.style_for_token(token_type)
                token_color = token_style['color']
                token_bg = token_style['bgcolor']

                # Si no hay color de fondo definido, aplicar uno por defecto
                if not token_bg:
                    token_bg = '2E3440'  # Fondo por defecto: gris oscuro para el tema material

                # Configurar el tag con foreground y background
                if token_color or token_bg:
                    text_area.tag_configure(tag_name, foreground=f"#{token_color}" if token_color else None,
                                            background=f"#{token_bg}" if token_bg else None)

            # Aplicar el tag al texto
            text_area.tag_add(tag_name, start_index, end_index)
            
            # Buscar la próxima aparición del mismo valor
            start_index = text_area.search(value, end_index, tk.END)

# Función para ejecutar el código en el editor
def ejecutar_codigo():
    """Ejecuta el código contenido en el área de texto."""
    try:
        # Obtener el contenido del área de texto
        codigo = text_area.get("1.0", tk.END)
        # Ejecutar el código usando exec
        exec(codigo)
    except Exception as e:
        # Mostrar un mensaje si hay un error en la ejecución
        messagebox.showerror("Error en la ejecución", str(e))

#-------------------------------------------------------------------------------------------------
# Crear el área de texto
text_area = tk.Text(root, undo=True, background="#2E3440", foreground="white", insertbackground="white",
                    font=("Consolas", 14))  # Consolas 14, fondo #2E3440

barra_desplazamiento = tk.Scrollbar(text_area)  # Barra de desplazamiento para el área de texto

root.grid_rowconfigure(0, weight=1)  # Configurar el peso de la fila
root.grid_columnconfigure(0, weight=1)  # Configurar el peso de la columna

text_area.grid(sticky=tk.N + tk.E + tk.S + tk.W)  # Posicionar el área de texto

barra_desplazamiento.pack(side=tk.RIGHT, fill=tk.Y)  # Posicionar la barra de desplazamiento
text_area.config(yscrollcommand=barra_desplazamiento.set)  # Conectar la barra de desplazamiento al área de texto

# Vincular el evento de teclas para aplicar resaltado de sintaxis mientras se escribe
text_area.bind("<KeyRelease>", apply_syntax_highlighting)

archivo = None  # Variable para almacenar el nombre del archivo actual

# Crear la barra de menú
menu_bar = tk.Menu(root)  # Crear la barra de menú

# Menú Archivo
menu_archivo = tk.Menu(menu_bar, tearoff=0)  # Crear el menú Archivo
menu_bar.add_cascade(label="Archivo", menu=menu_archivo)  # Añadir menú Archivo a la barra
menu_archivo.add_command(label="Nuevo Archivo", command=nuevo_archivo)  # Opción para nuevo archivo
menu_archivo.add_command(label="Abrir Archivo", command=abrir_archivo)  # Opción para abrir archivo
menu_archivo.add_command(label="Guardar Archivo", command=guardar_archivo)  # Opción para guardar archivo
menu_archivo.add_separator()  # Separador en el menú
menu_archivo.add_command(label="Salir", command=salir)  # Opción para salir

# Menú Editar
menu_editar = tk.Menu(menu_bar, tearoff=0)  # Crear el menú Editar
menu_bar.add_cascade(label="Editar", menu=menu_editar)  # Añadir menú Editar a la barra
menu_editar.add_command(label="Cortar", command=cortar_texto)  # Opción para cortar texto
menu_editar.add_command(label="Copiar", command=copiar_texto)  # Opción para copiar texto
menu_editar.add_command(label="Pegar", command=pegar_texto)  # Opción para pegar texto

# Menú Buscar (Opciones adicionales pueden ser agregadas aquí)
menu_buscar = tk.Menu(menu_bar, tearoff=0)  # Crear el menú Buscar
menu_bar.add_cascade(label="Buscar", menu=menu_buscar)  # Añadir menú Buscar a la barra

# Menú Ver (Opcional para futuras funciones)
menu_ver = tk.Menu(menu_bar, tearoff=0)  # Crear el menú Ver
menu_bar.add_cascade(label="Ver", menu=menu_ver)  # Añadir menú Ver a la barra

# Menú Ejecutar (Opción para ejecutar el código del editor)
menu_ejecutar = tk.Menu(menu_bar, tearoff=0)  # Crear el menú Ejecutar
menu_ejecutar.add_command(label="Ejecutar código", command=ejecutar_codigo)  # Opción para ejecutar código
menu_bar.add_cascade(label="Ejecutar", menu=menu_ejecutar)  # Añadir menú Ejecutar a la barra

# Menú Acerca de (Información sobre la aplicación puede ser añadida aquí)
menu_acerca = tk.Menu(menu_bar, tearoff=0)  # Crear el menú Acerca de
menu_bar.add_cascade(label="Acerca de", menu=menu_acerca)  # Añadir menú Acerca de a la barra

# Configurar la barra de menú
root.config(menu=menu_bar)  # Asignar la barra de menú a la ventana

# Iniciar el loop principal de la aplicación
root.mainloop()  # Ejecutar la aplicación
