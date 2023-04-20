import socket
import os

# Configuración del servidor
HOST = '192.168.43.250'  # Dirección IP del servidor
PORT = 12345  # Puerto utilizado por el servidor
DIRECTORY = './audio_files/'  # Directorio donde se guardarán los archivos de audio recibidos
buffer_size = 1024
# Crear el socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creamos nuestro socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) # Creamos el canal de comunicación entre el puerto y el socket
server_socket.listen() # Pone el estado del protocolo en listo, empieza a aceptar las conecciones y recibir las solicitudes

print(f'Servidor escuchando en {HOST}:{PORT}...')

# Configurar el socket como no bloqueante
server_socket.setblocking(0)

# Lista de clientes conectados
clients = []

while True:
    # Aceptar nuevas conexiones de clientes
    # Ocupé try por si llega a ocurrir un error
    try:
        client_socket, address = server_socket.accept() # Se genera la conexion
        print(f'Conexión aceptada de {address}')
        
        # Configurar el socket del cliente como no bloqueante
        client_socket.setblocking(0)
        
        # Agregar el cliente a la lista de clientes
        clients.append(client_socket)
    except socket.error:
        pass
    
    # Leer datos de los clientes conectados
    for client_socket in clients:
        try:
            audio = client_socket.recv(buffer_size)
            if audio:
                # Recibir un archivo de audio
                # Ocupé os.path para poder darles un nombre a los archivos que se están recibiendo
                # os.path.join es para juntar rutas
                # getpeername -- > retorna la dirección [0] a la que está conectado el socket y el puerto [1]
                audio_recibido = os.path.join(DIRECTORY, f'{client_socket.getpeername()[0]}_{client_socket.getpeername()[1]}.mp3')
                with open(audio_recibido, 'wb') as f:
                    f.write(audio)
                print(f'Archivo de audio recibido de {client_socket.getpeername()} y guardado en {audio_recibido}')
                # Enviar una confirmación al cliente
                client_socket.sendall(b'Archivo de audio recibido y guardado correctamente\n')
            else:
                # Si no hay datos, el cliente se desconectó
                print(f'{client_socket.getpeername()} desconectado')
                client_socket.close()
                clients.remove(client_socket)
        except socket.error:
            pass

