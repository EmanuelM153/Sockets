# Se importan las librerías necesarias
import socket
import multiprocessing

# La función que cada hilo ejecuta
def handle_client(client_socket):
    # Se reciben máximo 1024 bytes del socket
    request = client_socket.recv(1024)
    # Se imprimen los datos recibidos
    # Se decodifican los datos y se vuelven texto ya que son un objeto Bytes de Python
    print(f"Recibido: {request.decode()}")
    # Se envía un mensaje al cliente junto a una parte de la cabecera HTTP
    # Nótese el uso de la `b` ya que se deben enviar bytes
    client_socket.send(b"HTTP/1.1 200 OK\n\nHola, cliente!")
    # Se termina la comunicación, i.e., se cierra el descriptor del archivo del socket
    client_socket.close()

# Se crea un objeto Socket de Python
# En el constructor se especifica que la familia de direcciones sea IPv4 y que el tipo de socket sea para comunicaciones TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Se asocia el socket a la dirección 0.0.0.0, que corresponde a la dirección por defecto, y al puerto 8080
server.bind(("0.0.0.0", 8080))
# Se habilita el servidor, y se establece que 5 van a ser el número de conexiones inaceptables que el sistema permite antes de que rechazen nuevas conexiones
server.listen(5)
print("Servidor escuchando en puerto 8080...")

# En un bucle infinito:
while True:
    # Se espera por una conexión y cuando se acepta, se recibe un nuevo objeto tipo Socket (cliente_socket) y la dirección del cliente (addr)
    client_socket, addr = server.accept()
    print(f"Conexión desde {addr}")
    # Se crea un proceso con la función `handle_client` y con argumento del nuevo objeto Socket
    client_process = multiprocessing.Process(target=handle_client, args=(client_socket,))
    # Se inicia el proceso
    client_process.start()
