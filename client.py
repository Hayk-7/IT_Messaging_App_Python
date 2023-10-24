import socket
import threading
import time


class Client:
    def __init__(self):
        # HEADER = Information about the message to be received (in this case, the length of the message)
        self.HEADER = 64
        # FORMAT = The format (encryption) of the messages
        self.FORMAT = "utf-8"
        self.DEFAULT_PORT = 6969
        self.DISCONNECT_MESSAGE = "/dc"
        self.SERVER = None

        self.listener = None
        self.sender = None
        self.login = None
        self.connected = None
        self.client = None

    def connect(self):
        self.SERVER = self.findServerHome()

        # Socket = endpoint that receives data
        # Create a socket object (AF_INET = IPv4, SOCK_STREAM = TCP)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port 6969
        self.client.connect((self.SERVER, self.DEFAULT_PORT))
        self.client.send(bytes("PERMANENT", self.FORMAT))
        self.connected = True

        # Get connected message from the server
        msg = self.client.recv(128)
        print(msg.decode(self.FORMAT))

        # Send login to the server
        self.login = input("Login: ")
        self.client.send(bytes(self.login, self.FORMAT))

        # Listen for messages from the server and be able to send messages to the server at the same time using
        # threading
        self.sender = threading.Thread(target=self.Send)
        self.sender.start()
        self.listener = threading.Thread(target=self.listen)
        self.listener.start()

    # Scan local network for open port DEFAULT_PORT
    def findServerSchool(self):
        s = time.time()
        for x1 in range(134, 136):
            for x2 in range(100):
                for x3 in range(100):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.0001)
                    print(f"Trying: 10.{x1}.{x2}.{x3}:{self.DEFAULT_PORT}")
                    result = sock.connect_ex((f"10.{x1}.{x2}.{x3}", self.DEFAULT_PORT))
                    if result == 0:
                        e = time.time()
                        print(f"Found: 10.{x1}.{x2}.{x3} in {e - s}s")
                        sock.close()
                        return f"10.{x1}.{x2}.{x3}"
        sock.close()
        print("No server found")

    def findServerHome(self):
        s = time.time()
        for x1 in range(30, 169):
            for x2 in range(32,33):
                for x3 in range(100):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.0001)
                    print(f"Trying: 172.{x1}.{x2}.{x3}:{self.DEFAULT_PORT}")
                    result = sock.connect_ex((f"172.{x1}.{x2}.{x3}", self.DEFAULT_PORT))
                    if result == 0:
                        e = time.time()
                        print(f"Found: 172.{x1}.{x2}.{x3} in {e - s}s")
                        sock.close()
                        return f"172.{x1}.{x2}.{x3}"
        sock.close()
        print("No server found")

    def findServerHotspot(self):
        s = time.time()
        for x1 in range(10, 11):
            for x2 in range(22, 23):
                for x3 in range(94, 95):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.0001)
                    print(f"Trying: 26.{x1}.{x2}.{x3}:{self.DEFAULT_PORT}")
                    result = sock.connect_ex((f"26.{x1}.{x2}.{x3}", self.DEFAULT_PORT))
                    if result == 0:
                        e = time.time()
                        print(f"Found: 26.{x1}.{x2}.{x3} in {e - s}s")
                        sock.close()
                        return f"26.{x1}.{x2}.{x3}"
        sock.close()
        print("No server found")

    def send(self, msg):
        # Encode the message
        message = msg.encode(self.FORMAT)
        # Get the length of the message
        msg_length = len(message)
        # Encode the length of the message
        send_length = str(msg_length).encode(self.FORMAT)
        # Add spaces to the length of the message to make it 64 characters long
        send_length += b' ' * (self.HEADER - len(send_length))
        # Send the length of the message
        self.client.send(send_length)
        # Send the message
        self.client.send(message)

        # Wait for the server to confirm that the message was received
        # rmsg = client.recv(128)
        # print(rmsg.decode(FORMAT))

    def receive(self):
        # Receive length of the message from the client
        msg_length = int(self.client.recv(self.HEADER).decode(self.FORMAT))
        if msg_length:
            # Receive data from the client
            msg = self.client.recv(msg_length).decode(self.FORMAT)
            print(msg)

    def listen(self):
        while self.connected:
            self.receive()

    def Send(self):
        while self.connected:
            message = input()
            if message == self.DISCONNECT_MESSAGE:
                self.connected = False
            self.send(message)
