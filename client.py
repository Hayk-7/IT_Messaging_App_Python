import socket

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


def send(msg):
    # Send the length of the message
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # Add spaces to the length of the message to make it 64 characters long
    send_length += b' ' * (HEADER - len(send_length))
    # Send the length of the message
    client.send(send_length)
    # Send the message
    client.send(message)


# Get connected message from the server
msg = client.recv(128)
print(msg.decode(FORMAT))

while True:
    # Get the message from the user
    message = input("Enter the message: ")
    # Send the message to the server
    send(message)
    # If the user sends the DISCONNECT_MESSAGE, disconnect the client
    if message == DISCONNECT_MESSAGE:
        break

    # Wait for the server to confirm that the message was received
    msg = client.recv(128)
    print(msg.decode(FORMAT))
