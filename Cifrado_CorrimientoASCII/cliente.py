import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import socket


# Generar y guardar la clave de cifrado
def generar_clave():
    clave = Fernet.generate_key()
    with open("clave.key", "wb") as archivo_clave:
        archivo_clave.write(clave)

# Cargar la clave de cifrado
def cargar_clave():
    return open("clave.key", "rb").read()

#Enviar solicitud al servidor
def enviar_solicitud(servidor, request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((servidor, 9999))
    client_socket.sendall(request.encode('utf-8'))
    return client_socket


# Cifrar el contenido del archivo y guardar en un nuevo archivo
def cifrar(archivo, clave, server_socket):
    f = Fernet(clave)
    with open(archivo, "rb") as file:
        archivo_datos = file.read()
    datos_cifrados = f.encrypt(archivo_datos)
    nuevo_nombre = archivo.replace(".", "_c.")
    with open(nuevo_nombre, "wb") as file:
        file.write(datos_cifrados)
    mostrar_contenido(nuevo_nombre)
    #Se envian los datos al servidor
    server_socket.sendall('upload;'.encode('utf-8'))
    server_socket.sendall(f'{archivo};'.encode('utf-8'))
    server_socket.sendall(datos_cifrados)


# Funcion para cifrar el archivo
def cifrar_archivo():
    clave = cargar_clave()
    archivo = filedialog.askopenfilename(filetypes=[("Text files", ".txt"), ("PDF files", ".pdf")])
    if archivo:
        client_socket = enviar_solicitud('localhost', 'upload')
        cifrar(archivo, clave, client_socket)
        messagebox.showinfo("Información", "Archivo cifrado con éxito")


# Función para mostrar el contenido del archivo
def mostrar_contenido(archivo):
    with open(archivo, "r") as file:
        contenido = file.read()
        texto_contenido.delete(1.0, tk.END)
        texto_contenido.insert(tk.END, contenido)

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Cifrado y Descifrado de Archivos")

boton_cifrar = tk.Button(ventana, text="Cifrar y Enviar Archivo", command=cifrar_archivo)
boton_cifrar.pack(pady=5)

# Agregar un widget Text para mostrar el contenido
texto_contenido = tk.Text(ventana, height=10, width=50)
texto_contenido.pack(pady=10)

# Generar clave al iniciar la aplicación
generar_clave()

ventana.mainloop()
