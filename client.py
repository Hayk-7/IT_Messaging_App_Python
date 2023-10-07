import socket
DEFAULT_PORT = 6969
# Socket = endpoint that receives data

# Create a socket object (AF_INET = IPv4, SOCK_STREAM = TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port 6969
s.connect((socket.gethostname(), DEFAULT_PORT))


while True:
    # Receive data from the server (1024 = buffer size)
    msg = s.recv(1024)
    # Print the data received from the server (Data is sent under the form of bytes, so we need to decode it (using
    # utf-8))
    print(msg.decode("utf-8"))
