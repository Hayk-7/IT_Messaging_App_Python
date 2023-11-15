import socket
import threading
import time


class Client:
    def __init__(self, LOGIN):
        # HEADERLEN = Information about the message to be received (in this case, the length of the message)
        self.HEADERLEN = 64
        # FORMAT = The format (encryption) of the messages
        self.FORMAT = "utf-8"
        self.DEFAULT_PORT = 6969
        self.DISCONNECT_MESSAGE = "/dc"
        self.SERVER = None

        self.listener = None
        self.sender = None
        self.login = LOGIN
        self.connected = None

        # Socket = endpoint that receives data
        # Create a socket object (AF_INET = IPv4, SOCK_STREAM = TCP)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.message_list = []
        self.newMessage = False
        self.loadChatFile = False

    def connect(self):
        self.SERVER = self.findServerSchool()

        # Connect the socket to the port 6969
        self.client.connect((self.SERVER, self.DEFAULT_PORT))
        self.client.send(bytes("PERMANENT", self.FORMAT))
        self.connected = True

        # Get connected message from the server
        msg = self.client.recv(128)
        print(msg.decode(self.FORMAT))

        self.client.send(bytes(self.login, self.FORMAT))

        # Listen for messages from the server and be able to send messages to the server at the same time using
        # threading
        self.listener = threading.Thread(target=self.listen)
        self.listener.start()

    # Scan local network for open port DEFAULT_PORT
    def findServerSchool(self):
        s = time.time()
        for x1 in range(134, 136):
            for x2 in range(53,55):
                for x3 in range(133, 135):
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
        for x1 in range(168, 169):
            for x2 in range(100):
                for x3 in range(100):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.0001)
                    print(f"Trying: 192.{x1}.{x2}.{x3}:{self.DEFAULT_PORT}")
                    result = sock.connect_ex((f"192.{x1}.{x2}.{x3}", self.DEFAULT_PORT))
                    if result == 0:
                        e = time.time()
                        print(f"Found: 192.{x1}.{x2}.{x3} in {e - s}s")
                        sock.close()
                        return f"192.{x1}.{x2}.{x3}"
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
        send_length += b' ' * (self.HEADERLEN - len(send_length))
        # Send the length of the message
        self.client.send(send_length)
        # Send the message
        self.client.send(message)

    def receive(self):
        # Get the type of message (0 -> message, 1 -> messageList)
        try:
            msg_type = int(self.client.recv(1).decode(self.FORMAT))
        except:
            return
        if msg_type == 0:
            msg_length = int(self.client.recv(self.HEADERLEN).decode(self.FORMAT))
            if msg_length:
                # Receive data from the server
                msg = self.client.recv(msg_length).decode(self.FORMAT)
                if msg == "LoadChatFile":
                    self.loadChatFile = True
        elif msg_type == 1:
            # Empty the message list
            self.message_list = []
            # Get the length of the list
            list_length = int(self.client.recv(self.HEADERLEN).decode(self.FORMAT))
            # Loop through the list
            for message in range(list_length):
                # Verify that the login is of type message (0)
                if self.client.recv(1).decode(self.FORMAT) != "0":
                    return
                # Get the length of the login
                login_length = int(self.client.recv(self.HEADERLEN).decode(self.FORMAT))
                # Get the login
                login = self.client.recv(login_length).decode(self.FORMAT)
                # Verify that the message is of type message (0)
                if self.client.recv(1).decode(self.FORMAT) != "0":
                    return
                # Get the length of the message
                msg_length = int(self.client.recv(self.HEADERLEN).decode(self.FORMAT))
                # Get the message
                msg = self.client.recv(msg_length).decode(self.FORMAT)
                # Add the login and message to the message list
                self.message_list.append((login, msg))

            # Set newMessage to True so that the interface can display the messages
            self.newMessage = True

    def listen(self):
        while self.connected:
            self.receive()
