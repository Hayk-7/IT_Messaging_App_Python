import socket
import threading

# HEADER = Information about the message to be received (in this case, the length of the message)
HEADER = 64
# FORMAT = The format (encryption) of the message to be received
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "/dc"
DEFAULT_PORT = 6969


# Get the IP address of the server
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, DEFAULT_PORT)


# Socket = endpoint that receives data
# Create a socket object (AF_INET = IPv4, SOCK_STREAM = TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port 6969
server.bind(ADDR)

client_list = []


def send(msg, conn):
    # Encode the message
    message = msg.encode(FORMAT)
    # Get the length of the message
    msg_length = len(message)
    # Encode the length of the message
    send_length = str(msg_length).encode(FORMAT)
    # Add spaces to the length of the message to make it 64 characters long
    send_length += b' ' * (HEADER - len(send_length))
    # Send the length of the message
    conn.send(send_length)
    # Send the message
    conn.send(message)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    client_list.append(conn)
    # Send data to the client (Data is sent under the form of bytes, so we need to encode it (using utf-8))
    conn.send(bytes(f"Connected to the server {ADDR}", FORMAT))
    while connected:
        # Receive length of the message from the client
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if int(msg_length):
            # Receive data from the client
            msg = conn.recv(int(msg_length)).decode(FORMAT)
            # If the client sends the DISCONNECT_MESSAGE, disconnect the client
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            # Inform the client that the message was received
            # conn.send(bytes("Message received", FORMAT))

            # Send the message to all the clients
            for client in client_list:
                send(f"[{addr}] {msg}", client)
    # When out of while loop disconnect client
    print(f"[DISCONNECTED] {addr} disconnected.")
    client_list.remove(conn)
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # Accept the connection from the client
        conn, address = server.accept()
        # Create a thread for each client (to handle multiple clients)
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Server is starting...")
start()


