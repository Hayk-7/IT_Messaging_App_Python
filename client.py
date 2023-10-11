import socket
import threading
import time

# HEADER = Information about the message to be received (in this case, the length of the message)
HEADER = 64
# FORMAT = The format (encryption) of the message to be received
FORMAT = "utf-8"
DEFAULT_PORT = 6969
DISCONNECT_MESSAGE = "/dc"


# TESTING ---------------------------------------

# Scan local network for open port DEFAULT_PORT
def findServer():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", DEFAULT_PORT))
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    sock.close()
    return ip
    # s = time.time()
    # for x1 in range(134, 136):
    #     for x2 in range(100):
    #         for x3 in range(100):
    #             sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #             sock.settimeout(0.0001)
    #             print(f"Trying: 10.{x1}.{x2}.{x3}:{DEFAULT_PORT}")
    #             result = sock.connect_ex((f"10.{x1}.{x2}.{x3}", DEFAULT_PORT))
    #             if result == 0:
    #                 e = time.time()
    #                 print(f"Found: 10.{x1}.{x2}.{x3} in {e-s}")
    #                 return f"10.{x1}.{x2}.{x3}"
    #             sock.close()


SERVER = findServer()

# TESTING ---------------------------------------

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
        message = input()
        if message == DISCONNECT_MESSAGE:
            connected = False
        send(message)


# Listen for messages from the server and be able to send messages to the server at the same time using threading
sender = threading.Thread(target=Send)
sender.start()
listener = threading.Thread(target=listen)
listener.start()
