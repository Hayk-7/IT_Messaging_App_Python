"""
Code for the WhatsDown client side

Created on Sun Nov 23 00:00:00 1000
@author: H, R
"""

import socket
import threading
import time


class Client:
    """
    This class represents a client in the WhatsDown application.

    Attributes:
    - HEADERLEN: Length of the message header.
    - FORMAT: Format (encoding) of the messages.
    - DEFAULT_PORT: Default port number for communication.
    - DISCONNECT_MESSAGE: Message to initiate a disconnect.
    - SERVER: IP address of the server.
    - listener: Thread for listening to incoming messages.
    - login: Login information of the client.
    - connected: Flag indicating if the client is connected.
    - client: Socket object for communication.
    - message_list: List to store all messages.
    - newMessage: Flag indicating the presence of new messages.
    - loadChatFile: Flag indicating the need to load the chat file.

    Methods:
    - __init__: Initializes the client with provided login.
    - connect: Connects the client to the server and starts the listener thread.
    - findServerSchool: Scans the local network for the server's IP address.
    - findServerHome: Scans a home network for the server's IP address.
    - send: Sends a message to the server.
    - receive: Receives messages from the server and updates message_list.
    - listen: Continuously listens for incoming messages from the server.
    """
    def __init__(self, LOGIN):
        """
        Initializes the client with provided login.
        :param LOGIN:
        """
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
        """
        Connects the client to the server and starts the listener thread
        on specified port.
        """
        self.SERVER = self.findServerHome()

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
        """
        Scans the school network for the server's IP address.
        returns IP address of the server, if found.
        """
        s = time.time()
        for x1 in range(134, 178):  # Testing range
            for x2 in range(53,254):
                for x3 in range(197, 250):
                    ip = f"10.{x1}.{x2}.{x3}"
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # Times out quickly if the server is not found
                    sock.settimeout(0.0001)
                    print(f"[DEBUG] Trying: {ip}:{self.DEFAULT_PORT}")
                    # Tries to connect to each server (bruteforce search)
                    result = sock.connect_ex((ip, self.DEFAULT_PORT))
                    if result == 0:
                        e = time.time()
                        print(f"Found:{ip} in {e - s}s")
                        sock.close()
                        return ip
        sock.close()
        print("No server found")

    def findServerHome(self):
        """
        Scans the home network for the server's IP address.
        returns IP address of the server, if found.
        """
        s = time.time()
        for x1 in range(168, 169):
            for x2 in range(1, 100):
                for x3 in range(100):
                    ip = f"192.{x1}.{x2}.{x3}"
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # Times out quickly if the server is not found
                    sock.settimeout(0.0001)
                    print(f"[DEBUG] Trying: {ip}:{self.DEFAULT_PORT}")
                    # Tries to connect to each server (bruteforce search)
                    result = sock.connect_ex((ip, self.DEFAULT_PORT))
                    if result == 0:
                        e = time.time()
                        print(f"Found:{ip} in {e - s}s")
                        sock.close()
                        return ip
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
        """
        Receives messages from the server and updates message_list.
        """
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
        """
        Continuously listen for messages from the server
        """
        while self.connected:
            self.receive()
