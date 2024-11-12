# Se importan las librerías necesarias
import socket
import select

# Se crea un objeto Socket de Python
# En el constructor se especifica que la familia de direcciones sea IPv4 y que el tipo de socket sea para comunicaciones TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Se asocia el socket a la dirección 0.0.0.0, que corresponde a la dirección por defecto, y al puerto 8080
server.bind(("0.0.0.0", 8080))
# Se habilita el servidor, y se establece que 5 van a ser el número de conexiones inaceptables que el sistema permite antes de que rechazen nuevas conexiones
server.listen(5)
# Se crea una lista para monitorear las conexiones
sockets = [server]

# En un bucle infinito:
while True:
    # El método select es una interfaz para la llamada al sistema con el mismo nombre, que se encarga de hacer multiplexación de I/O de forma **sincrónica**
    # En esta línea, se pasa como argumento la lista de sockets y se bloquea el programa hasta que un descriptor de archivo se pueda leer, i.e., se recibió una conexión
    # Y se retorna la lista de sockets listos para ser leídos
    readable, _, _ = select.select(sockets, [], [])

    # Se itera por esta lista
    for s in readable:
        # Si el objeto es el mismo servidor
        if s is server:
            client_socket, addr = server.accept()
            # Se espera por una conexión y cuando se acepta, se recibe un nuevo objeto tipo Socket (cliente_socket) y la dirección del cliente (addr)
            print(f"Conexión desde {addr}")
            # Se agrega el nuevo socket a la lista de monitorización
            sockets.append(client_socket)
        # Si el objeto es un objeto Socket que representa la comunicación con el cliente
        else:
            # Se reciben máximo 1024 bytes del socket
            data = s.recv(1024)

            # Si hay datos
            if data:
                # Se imprimen los datos recibidos
                # Se decodifican los datos y se vuelven texto ya que son un objeto Bytes de Python
                print(f"Recibido: {data.decode()}")
                # Se envía un mensaje al cliente junto a una parte de la cabecera HTTP
                # Nótese el uso de la `b` ya que se deben enviar bytes
                s.send(b"HTTP/1.1 200 OK\n\nHola, cliente!")
            # Si no se recibieron datos
            else:
                print("Cliente desconectado")
                # Se remueve este objeto Socket de la lista de monitorización
                sockets.remove(s)
                # Se termina la comunicación, i.e., se cierra el descriptor del archivo del socket
                s.close()
