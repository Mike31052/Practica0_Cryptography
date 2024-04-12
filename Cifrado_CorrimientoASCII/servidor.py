import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import socket
import threading


def handle_client(client_socket):
    #Recibimos los datos del cliente
    
    #Recibimos el tipo de solicitud y el tamaño
    typeRequest_length = int(client_socket.recv(4).decode('utf-8'))
    typeRequest = client_socket.recv(typeRequest_length).decode('utf-8')
    print(f"Request: {typeRequest}, size: {typeRequest_length}")

    #Recibimos el nombre del archivo y el tamaño
    filename_length = int(client_socket.recv(4).decode('utf-8'))
    filename = client_socket.recv(filename_length).decode('utf-8')
    print(f"FileName: {filename}, size: {filename_length}")

    #Recibimos la clave
    clave_length = int.from_bytes(client_socket.recv(4), 'big')
    clave = client_socket.recv(clave_length)
    print(f"Clave: {clave}, size: {clave_length}")

    #Recibimos los datos cifrados y la longitud
    data_c_length = int(client_socket.recv(4).decode('utf-8'))
    data_c = client_socket.recv(data_c_length).decode('utf-8')
    print(f"Data_c: {data_c}, size: {data_c_length}")

    if typeRequest == 'upload':
        receive_and_descif_file(clave, data_c, filename)
    client_socket.close()


# Función para recibir el archivo cifrado del cliente, descifrarlo y mostrar el contenido
def receive_and_descif_file(clave, data_c, filename):
    f = Fernet(clave)
    
    data_d = f.decrypt(data_c)

    nuevo_nombre = filename.replace(".", "_d.")
    with open(nuevo_nombre, 'wb') as file:
        file.write(data_d)

    mostrar_contenido(data_c, nuevo_nombre)

# Función para mostrar el contenido del archivo
def mostrar_contenido(data_c, archivo_d):
    texto_contenido_c.delete(1.0, tk.END)
    texto_contenido_c.insert(tk.END, data_c)
    with open(archivo_d, "r") as file:
        contenido_d = file.read()
        texto_contenido_d.delete(1.0, tk.END)
        texto_contenido_d.insert(tk.END, contenido_d)

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

# Widget text para texto cifrado
texto_contenido_c = tk.Text(ventana, height=10, width=50)
texto_contenido_c.pack(pady=10)

# Widget text para texto sin cifrar
texto_contenido_d = tk.Text(ventana, height=10, width=50)
texto_contenido_d.pack(pady=10)

# Iniciar el servidor en un hilo separado
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Iniciar el bucle de la interfaz
ventana.mainloop()
