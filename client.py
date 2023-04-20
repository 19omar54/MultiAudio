import socket
import time
# Configuración del cliente
HOST = '192.168.1.182'  # Dirección IP del servidor
PORT = 12345  # Puerto utilizado por el servidor
audio_enviar = 'audio1.mp3'  # Nombre del archivo de audio a enviar

# Crear el socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Configurar el socket como no bloqueante
# permite realizar múltiples operaciones
client_socket.setblocking(0)

# Leer el archivo de audio
with open(audio_enviar, 'rb') as f:  # rb --> abrir archivo solo para lectura en formato binario
    data = f.read()

# Enviar el archivo de audio al servidor
try:
    time.sleep(10)
    client_socket.sendall(data) # asegura que se envíen todos los datos, o hasta que ocurra un error
    print(f'Archivo de audio {audio_enviar} enviado al servidor {HOST}:{PORT}')
    
    # Leer la confirmación del servidor
    data = client_socket.recv(1024)
    print(data.decode())
except socket.error:
    pass

# Cerrar el socket
client_socket.close()