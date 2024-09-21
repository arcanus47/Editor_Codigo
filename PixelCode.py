import os
import codecs
import tempfile
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

#-------------------------------------------------------------------------------------------------
# Función para crear la barra de números de línea
def crear_barra_numeros_linea(padre):
    barra_numeros = tk.Text(padre, width=4, padx=3, state='disabled', takefocus=0, background="#2E3440", foreground="white")
    return barra_numeros

# Función para actualizar los números de línea
def actualizar_numeros_linea(evento=None):
    barra_numeros_linea.config(state='normal')
    barra_numeros_linea.delete(1.0, tk.END)
    linea_final, _ = text_area.index('end-1c').split('.')
    numeros_linea = "\n".join(str(i) for i in range(1, int(linea_final)))
    barra_numeros_linea.insert(1.0, numeros_linea)
    barra_numeros_linea.config(state='disabled')

#-------------------------------------------------------------------------------------------------
# Crear la ventana principal
root = tk.Tk()
root.state('zoomed')
root.title("PixelCode v0.6")
root.geometry("1024x500")

# Centralizar ventana
wventana, hventana = 1024, 500
pwidth = (root.winfo_screenwidth() // 2) - (wventana // 2)
pheight = (root.winfo_screenheight() // 2) - (hventana // 2)
root.geometry(f"{wventana}x{hventana}+{pwidth}+{pheight}")

#-------------------------------------------------------------------------------------------------
# Funciones para archivos, editar, ver, ejecutar
def nuevo_archivo():
    root.title("Untitled")
    text_area.delete(1.0, tk.END)

def cargar_archivo(archivo):
    """Carga el contenido de un archivo en el área de texto."""
    try:
        with open(archivo, "r") as archivo_abierto:
            contenido = archivo_abierto.read()
            text_area.delete(1.0, tk.END)  # Limpiar el área de texto
            text_area.insert('1.0', contenido)  # Insertar contenido en el área de texto
        root.title(os.path.basename(archivo))  # Cambiar el título a nombre del archivo
    except Exception as e:
        messagebox.showerror(message=f"No se puede leer el Archivo: {str(e)}", title="Error")

def abrir_archivo():
    """Abre un archivo de código existente y carga su contenido."""
    archivo = filedialog.askopenfilename(defaultextension=".py", 
                                         filetypes=[("Archivos de Código", "*.py")])
    if archivo:  # Si se seleccionó un archivo
        cargar_archivo(archivo)

def guardar_archivo():
    archivo = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Archivos de Código", "*.py")])
    if not archivo:
        return
    if not archivo.endswith(".py"):
        archivo += ".py"
    try:
        with open(archivo, "w") as archivo_guardado:
            contenido = text_area.get(1.0, tk.END)
            archivo_guardado.write(contenido)
        root.title(os.path.basename(archivo))
    except Exception as e:
        messagebox.showerror(message=f"No se puede guardar el archivo: {str(e)}", title="Error")

def imprimir():
    """Imprime el contenido del área de texto."""
    contenido = text_area.get(1.0, tk.END)

    # Crear un archivo temporal para la impresión
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
        temp_file.write(contenido.encode('utf-8'))
        temp_file_path = temp_file.name

    # Usar el comando de impresión del sistema
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['notepad.exe', '/p', temp_file_path])
        else:  # Unix (Linux, macOS)
            subprocess.run(['lp', temp_file_path])
    except Exception as e:
        messagebox.showerror(message=f"Error al imprimir: {str(e)}", title="Error")

def salir():
    """Cierra la aplicación."""
    respuesta = messagebox.askyesno("Salir", "¿Estás seguro de que deseas salir?")
    if respuesta:
        root.quit()

def deshacer():
    """Deshace la última acción."""
    text_area.edit_undo()

def rehacer():
    """Rehace la última acción deshecha."""
    text_area.edit_redo()
    
def cortar_texto():
    """Corta el texto seleccionado en el área de texto."""
    text_area.event_generate("<<Cut>>")

def copiar_texto():
    """Copia el texto seleccionado en el área de texto."""
    text_area.event_generate("<<Copy>>")

def pegar_texto():
    """Pega el texto del portapapeles en el área de texto."""
    text_area.event_generate("<<Paste>>")

def buscar():
    """Busca un texto en el área de texto."""
    busqueda = simpledialog.askstring("Buscar", "Texto a buscar:")
    if busqueda:
        start_index = text_area.search(busqueda, "1.0", tk.END)
        if start_index:
            end_index = f"{start_index}+{len(busqueda)}c"
            text_area.tag_add("highlight", start_index, end_index)
            text_area.mark_set("insert", end_index)
            text_area.see("insert")
        else:
            messagebox.showinfo("Buscar", "Texto no encontrado.")
            
def ir_a_la_linea():
    """Permite ir a una línea específica en el área de texto."""
    linea = simpledialog.askinteger("Ir a la línea", "Número de línea:")
    if linea:
        text_area.mark_set("insert", f"{linea}.0")
        text_area.see("insert")

def formato_archivos():
    """Permite seleccionar un formato de codificación para guardar el archivo."""
    opciones = ['UTF-8', 'ASCII', 'ISO-8859-1', 'UTF-16', 'Windows-1252']  # Lista de opciones de codificación

    # Crear una ventana emergente con las opciones de codificación
    formato = simpledialog.askstring("Formato de Archivo", "Selecciona el formato de codificación:\n" + "\n".join(opciones))

    if formato and formato in opciones:
        # Guardar el archivo con la codificación seleccionada
        archivo = filedialog.asksaveasfilename(defaultextension=".py",
                                               filetypes=[("Archivos de Código", "*.py")])
        if archivo:
            try:
                # Guardar el archivo con el formato seleccionado
                with codecs.open(archivo, "w", encoding=formato) as archivo_guardado:
                    contenido = text_area.get(1.0, tk.END)  # Obtener el contenido del área de texto
                    archivo_guardado.write(contenido)  # Escribir el contenido con la codificación seleccionada

                root.title(os.path.basename(archivo))  # Cambiar el título a nombre del archivo
                messagebox.showinfo("Guardado", f"Archivo guardado con formato {formato}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")
    else:
        messagebox.showwarning("Formato inválido", "Formato no válido o cancelado.")

def ampliar():
    """Aumenta el tamaño de la fuente."""
    current_font = text_area.cget("font").split()
    new_size = int(current_font[-1]) + 2
    text_area.config(font=("Consolas", new_size))

def reducir():
    """Disminuye el tamaño de la fuente."""
    current_font = text_area.cget("font").split()
    new_size = max(8, int(current_font[-1]) - 2)  # Evitar que el tamaño sea menor a 8
    text_area.config(font=("Consolas", new_size))

def restablecer():
    """Restablece el tamaño de la fuente al valor original."""
    text_area.config(font=("Consolas", 14))

# Variable global para almacenar el proceso de ejecución
proceso_ejecucion = None

# Función para ejecutar el código en el editor
def ejecutar_codigo():
    """Ejecuta el código contenido en el área de texto."""
    global proceso_ejecucion
    try:
        # Obtener el contenido del área de texto
        codigo = text_area.get("1.0", tk.END)

        # Crear un archivo temporal con el código
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp_file:
            temp_file.write(codigo.encode('utf-8'))
            temp_file_path = temp_file.name

        # Ejecutar el archivo usando subprocess.Popen para obtener un proceso separado
        proceso_ejecucion = subprocess.Popen(['python', temp_file_path],
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             text=True)

        # Leer la salida del proceso
        salida, error = proceso_ejecucion.communicate()

        if salida:
            print(salida)  # Mostrar salida en consola
        if error:
            messagebox.showerror("Error en la ejecución", error)  # Mostrar error en un mensaje

    except Exception as e:
        messagebox.showerror("Error en la ejecución", str(e))
        
def depurar():
    """Depura el código contenido en el área de texto."""
    codigo = text_area.get("1.0", tk.END)
    # Aquí podrías integrar herramientas como 'pdb' o lanzar un depurador.
    try:
        exec(codigo)  # Ejecutar el código y ver errores en consola
        messagebox.showinfo("Depurar", "El código se ejecutó correctamente.")
    except Exception as e:
        messagebox.showerror("Depuración", f"Error: {str(e)}")

def detener():
    """Detiene la ejecución del código."""
    global proceso_ejecucion
    if proceso_ejecucion and proceso_ejecucion.poll() is None:  # Si el proceso aún está corriendo
        proceso_ejecucion.terminate()  # Detener el proceso
        messagebox.showinfo("Ejecución detenida", "El código fue detenido.")
    else:
        messagebox.showinfo("Detener", "No hay ningún código en ejecución.")

# Función para aplicar el resaltado de sintaxis
def apply_syntax_highlighting(event=None):
    text_content = text_area.get("1.0", tk.END)
    text_area.tag_remove("highlight", "1.0", tk.END)  # Limpiar resaltado anterior
    lexer = PythonLexer()
    tokens = lex(text_content, lexer)
    style = get_style_by_name("material")
    
    for token_type, value in tokens:
        start_index = text_area.search(value, "1.0", tk.END)
        while start_index:
            end_index = f"{start_index}+{len(value)}c"
            tag_name = str(token_type)

            if tag_name not in text_area.tag_names():
                token_style = style.style_for_token(token_type)
                token_color = token_style['color']
                token_bg = token_style['bgcolor'] or '2E3440'
                text_area.tag_configure(tag_name, foreground=f"#{token_color}" if token_color else None,
                                                            background=f"#{token_bg}")

            text_area.tag_add(tag_name, start_index, end_index)
            start_index = text_area.search(value, end_index, tk.END)

#-------------------------------------------------------------------------------------------------
# Crear área de texto y barra de números de línea
frame_texto = tk.Frame(root)
frame_texto.pack(fill=tk.BOTH, expand=True)

barra_numeros_linea = crear_barra_numeros_linea(frame_texto)
barra_numeros_linea.pack(side=tk.LEFT, fill=tk.Y)

text_area = tk.Text(frame_texto, undo=True, background="#2E3440", foreground="white", insertbackground="white",
                    font=("Consolas", 14), wrap="none")
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Crear barra de desplazamiento
barra_desplazamiento = tk.Scrollbar(frame_texto, orient=tk.VERTICAL, command=text_area.yview)
barra_desplazamiento.pack(side=tk.RIGHT, fill=tk.Y)

text_area.config(yscrollcommand=barra_desplazamiento.set)
barra_numeros_linea.config(yscrollcommand=barra_desplazamiento.set)

# Vincular eventos de teclado
text_area.bind("<KeyRelease>", lambda event: [actualizar_numeros_linea(), apply_syntax_highlighting()])

# Crear la barra de menú
menu_bar = tk.Menu(root)  # Crear la barra de menú

# Menú Archivo
menu_archivo = tk.Menu(menu_bar, tearoff=0)  # Crear el menú Archivo
menu_bar.add_cascade(label="Archivo", menu=menu_archivo)  # Añadir menú Archivo a la barra
menu_archivo.add_command(label="Nuevo", command=nuevo_archivo)  # Opción para nuevo archivo
menu_archivo.add_command(label="Abrir", command=abrir_archivo)  # Opción para abrir archivo
menu_archivo.add_separator()  # Separador en el menú
menu_archivo.add_command(label="Guardar", command=guardar_archivo)  # Opción para guardar archivo
menu_archivo.add_separator()  # Separador en el menú
menu_archivo.add_command(label="Imprimir", command=imprimir)  # Opción para imprimir
menu_archivo.add_separator()  # Separador en el menú
menu_archivo.add_command(label="Salir", command=salir)  # Opción para salir

# Menú Editar
menu_editar = tk.Menu(menu_bar, tearoff=0)  # Crear el menú Editar
menu_bar.add_cascade(label="Editar", menu=menu_editar)  # Añadir menú Editar a la barra
menu_editar.add_command(label="Deshacer", command=deshacer)  # Opción para deshacer
menu_editar.add_command(label="Rehacer", command=rehacer)  # Opción para rehacer
menu_editar.add_separator()  # Separador en el menú
menu_editar.add_command(label="Cortar", command=cortar_texto)  # Opción para cortar texto
menu_editar.add_command(label="Copiar", command=copiar_texto)  # Opción para copiar texto
menu_editar.add_command(label="Pegar", command=pegar_texto)  # Opción para pegar texto
menu_editar.add_separator()  # Separador en el menú
menu_editar.add_command(label="Buscar", command=buscar)  # Opción para buscar
menu_editar.add_separator()  # Separador en el menú
menu_editar.add_command(label="Ir a la Línea", command=ir_a_la_linea)  # Opción para ir a la línea
menu_editar.add_separator()  # Separador en el menú
menu_editar.add_command(label="Formato de Archivos", command=formato_archivos)  # Opción para formato de archivos

# Menú Ver
menu_ver = tk.Menu(menu_bar, tearoff=0)  # Crear el menú Ver
menu_bar.add_cascade(label="Ver", menu=menu_ver)  # Añadir menú Ver a la barra
menu_ver.add_command(label="Ampliar", command=ampliar)  # Opción para ampliar
menu_ver.add_command(label="Reducir", command=reducir)  # Opción para reducir
menu_ver.add_command(label="Restablecer", command=restablecer)  # Opción para restablecer

# Menú Ejecutar
menu_ejecutar = tk.Menu(menu_bar, tearoff=0)  # Crear el menú Ejecutar
menu_bar.add_cascade(label="Ejecutar", menu=menu_ejecutar)  # Añadir menú Ejecutar a la barra
menu_ejecutar.add_command(label="Ejecutar código", command=ejecutar_codigo)  # Opción para ejecutar código
menu_ejecutar.add_command(label="Depurar", command=depurar)  # Opción para depurar
menu_ejecutar.add_command(label="Detener", command=detener)  # Opción para detener

# Menú Acerca de (Información sobre la aplicación puede ser añadida aquí)
menu_acerca = tk.Menu(menu_bar, tearoff=0)  # Crear el menú Acerca de
menu_bar.add_cascade(label="Acerca de", menu=menu_acerca)  # Añadir menú Acerca de a la barra

# Configurar la barra de menú
root.config(menu=menu_bar)  # Asignar la barra de menú a la ventana

# Iniciar el loop principal de la aplicación
root.mainloop()  # Ejecutar la aplicación
