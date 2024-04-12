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
def enviar_solicitud(servidor):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((servidor, 9999))
    return client_socket


# Cifrar el contenido del archivo y guardar en un nuevo archivo
#Fernet utiliza el algoritmo AES para cifrar y pertenece a los cifradores de bloque
def cifrar(archivo, clave, server_socket):
    
    print(f"Clave: {clave}")
    f = Fernet(clave)
    with open(archivo, "rb") as file:
        archivo_datos = file.read()
    datos_cifrados = f.encrypt(archivo_datos)
    nuevo_nombre = archivo.replace(".", "_c.")
    with open(nuevo_nombre, "wb") as file:
        file.write(datos_cifrados)

    #Mostrar el contenido cifrado
    mostrar_contenido(archivo, nuevo_nombre)

    #Se envian los datos al servidor
    #Se envia el tipo de solicitud y su longitud
    server_socket.sendall(str(len("upload")).zfill(4).encode('utf-8'))
    server_socket.sendall('upload'.encode('utf-8'))

    #Se envia el nombre del archivo y su longitud en bytes
    server_socket.sendall(str(len(archivo)).zfill(4).encode('utf-8'))
    server_socket.sendall(f'{archivo}'.encode('utf-8'))

    #Se envia la clave y su longitud en bytes
    server_socket.sendall(len(clave).to_bytes(4, 'big'))
    server_socket.sendall(clave)

    #Se envian los datos cifrados y su longitud
    server_socket.sendall(str(len(datos_cifrados)).zfill(4).encode('utf-8'))
    server_socket.sendall(datos_cifrados)


# Funcion para cifrar el archivo
def cifrar_archivo():
    clave = cargar_clave()
    archivo = filedialog.askopenfilename(filetypes=[("Text files", ".txt"), ("PDF files", ".pdf")])
    if archivo:
        client_socket = enviar_solicitud('localhost')
        cifrar(archivo, clave, client_socket)
        messagebox.showinfo("Información", "Archivo cifrado con éxito")


# Función para mostrar el contenido del archivo
def mostrar_contenido(archivo_d, archivo_c):
    with open(archivo_d, "r") as file:
        contenido_d = file.read()
        texto_contenido_d.delete(1.0, tk.END)
        texto_contenido_d.insert(tk.END, contenido_d)
    with open(archivo_c, "r") as file:
        contenido_c = file.read()
        texto_contenido_c.delete(1.0, tk.END)
        texto_contenido_c.insert(tk.END, contenido_c)

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Cifrado y Descifrado de Archivos")

boton_cifrar = tk.Button(ventana, text="Cifrar y Enviar Archivo", command=cifrar_archivo)
boton_cifrar.pack(pady=5)

# Widget text para texto sin cifrar
texto_contenido_d = tk.Text(ventana, height=10, width=50)
texto_contenido_d.pack(pady=10)

# Widget text para texto cifrado
texto_contenido_c = tk.Text(ventana, height=10, width=50)
texto_contenido_c.pack(pady=10)

# Generar clave al iniciar la aplicación
generar_clave()

ventana.mainloop()
