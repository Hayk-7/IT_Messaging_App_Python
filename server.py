import socket
DEFAULT_PORT = 6969
# Socket = endpoint that receives data

# Create a socket object (AF_INET = IPv4, SOCK_STREAM = TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port 6969
s.bind((socket.gethostname(), DEFAULT_PORT))
# Listen to the socket (5 = number of unaccepted connections that the system will allow before refusing new connections)
s.listen(5)


while True:
    # Accept the connection from the client
    clientsocket, address = s.accept()
    print(f"Connection from {address} established!")
    # Send data to the client (Data is sent under the form of bytes, so we need to encode it (using utf-8))
    clientsocket.send(bytes("Connected to the server", "utf-8"))
