import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import socket
import threading

# Cargar la clave de cifrado
def cargar_clave():
    return open("clave.key", "rb").read()


def handle_client(client_socket):
    data = client_socket.recv(1024).decode('utf-8')
    print(f"Received data: {data}")
    parts = data.split(';')
    request = parts[0]
    if request == 'upload':
        filename = parts[1]
        receive_and_descif_file(client_socket, filename)
    client_socket.close()


# Función para recibir el archivo cifrado del cliente, descifrarlo y mostrar el contenido
def receive_and_descif_file(client_socket, filename):
    clave = cargar_clave()
    f = Fernet(clave)

    data = client_socket.recv(1024)
    with open(filename, 'wb') as file:
        while data:
            file.write(data)
            data = client_socket.recv(1024)

    with open(filename, 'rb') as file:
        encrypted_data = file.read()

    decrypted_data = f.decrypt(encrypted_data)

    nuevo_nombre = filename.replace("_c.", "_d.")
    with open(nuevo_nombre, 'wb') as file:
        file.write(decrypted_data)

    mostrar_contenido(nuevo_nombre)

# Función para mostrar el contenido del archivo
def mostrar_contenido(archivo):
    with open(archivo, "r") as file:
        contenido = file.read()
        texto_contenido.delete(1.0, tk.END)
        texto_contenido.insert(tk.END, contenido)

# Configuramos el servidor y lo levantamos
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)

    print('[INFO] Server listening on port 9999...')

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Crear la interfaz gráfica
ventana = tk.Tk()
ventana.title("Cifrado y Descifrado de Archivos")

# Agregar un widget Text para mostrar el contenido
texto_contenido = tk.Text(ventana, height=10, width=50)
texto_contenido.pack(pady=10)

# Iniciar el servidor en un hilo separado
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Iniciar el bucle de la interfaz
ventana.mainloop()
