import socket
import threading

# HEADER = Information about the message to be received (in this case, the length of the message)
HEADER = 64
# FORMAT = The format (encryption) of the message to be received
FORMAT = "utf-8"
DEFAULT_PORT = 6969
DISCONNECT_MESSAGE = "/dc"
# Change the ip address to the server ip address
# TODO: Automatically get the ip address of the server
SERVER = "192.168.1.1"

# Socket = endpoint that receives data
# Create a socket object (AF_INET = IPv4, SOCK_STREAM = TCP)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port 6969
client.connect((SERVER, DEFAULT_PORT))
connected = True


def send(msg):
    # Encode the message
    message = msg.encode(FORMAT)
    # Get the length of the message
    msg_length = len(message)
    # Encode the length of the message
    send_length = str(msg_length).encode(FORMAT)
    # Add spaces to the length of the message to make it 64 characters long
    send_length += b' ' * (HEADER - len(send_length))
    # Send the length of the message
    client.send(send_length)
    # Send the message
    client.send(message)

    # Wait for the server to confirm that the message was received
    # rmsg = client.recv(128)
    # print(rmsg.decode(FORMAT))


def receive():
    # Receive length of the message from the client
    msg_length = int(client.recv(HEADER).decode(FORMAT))
    if msg_length:
        # Receive data from the client
        msg = client.recv(msg_length).decode(FORMAT)
        print(msg)


# Get connected message from the server
msg = client.recv(128)
print(msg.decode(FORMAT))


def listen():
    global connected
    while connected:
        receive()


def Send():
    global connected
    while connected:
        message = input("Enter message: ")
        if message == DISCONNECT_MESSAGE:
            connected = False
        send(message)


# Listen for messages from the server and be able to send messages to the server at the same time using threading
sender = threading.Thread(target=Send)
sender.start()
listener = threading.Thread(target=listen)
listener.start()

