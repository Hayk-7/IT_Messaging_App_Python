import socket
import threading

DEFAULT_PORT = 6969
# Get the IP address of the server
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, DEFAULT_PORT)


# Socket = endpoint that receives data
# Create a socket object (AF_INET = IPv4, SOCK_STREAM = TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port 6969
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    # Send data to the client (Data is sent under the form of bytes, so we need to encode it (using utf-8))
    conn.send(bytes(f"Connected to the server {ADDR}", "utf-8"))
    while connected:
        # Receive data from the server (1024 = buffer size)
        msg = conn.recv(1024)
        # Print the data received from the server (Data is sent under the form of bytes, so we need to decode it (using
        # utf-8))
        print(msg.decode("utf-8"))


def start():
    server.listen()
    while True:
        # Accept the connection from the client
        conn, address = server.accept()
        # Create a thread for each client (to handle multiple clients)
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Server is starting...")
start()


