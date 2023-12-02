"""
Code for the WhatsDown server side.

Created on Sun Nov 23 00:00:00 1000
@author: H, R

server.py

This module implements a simple chat server using sockets and threading.
Clients can connect to the server, send and receive messages, and the server
handles storing and retrieving messages between clients.

Constants:
- HEADERLEN: Information about the message to be received
(in this case, the length of the message)
- MSG: Represents a message type (0)
- MSGLIST: Represents a message list type (1)
- FORMAT: The format (encryption) of the message to be received
- DISCONNECT_MESSAGE: Special message to disconnect from the server
- DEFAULT_PORT: Default port number for the server
- SERVER: IP address of the server
- ADDR: Tuple containing the server IP address and port

Functions:
- sendMessage(msg, conn): Sends a single message to the specified connection.
- sendMessageList(msg_list, conn): Sends a list of messages to the specified
connection.
- saveMessageList(msg_list): Saves the list of messages to a file named after
the users in the conversation.
- loadMessageList(users): Loads the list of messages from a file based on the
users in the conversation.
- handleClient(conn, addr): Handles communication with a connected client,
managing message exchange and storage.
- start(): Starts the server, listens for incoming connections, and handles
each connection in a separate thread.

Usage:
- Run this script to start the chat server. Clients can connect to the server
to exchange messages.
"""

import socket
import threading
import os.path

# HEADERLEN = Information about the message to be received (in this case,
# the length of the message)
HEADERLEN = 64
# Send type -> 0 = message, 1 = messageList
MSG = "0"
MSGLIST = "1"

# FORMAT = The format (encryption) of the message to be received
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "/dc"  # Message to disconnect from the server
DEFAULT_PORT = 7070  # Default port number for the server

# Get the IP address of the server
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, DEFAULT_PORT)

# Socket = endpoint that receives data
# Create a socket object (AF_INET = IPv4, SOCK_STREAM = TCP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port 7070
server.bind(ADDR)

client_list = {}
message_list = []


def sendMessage(msg, conn):
    """
    Sends a message to the specified connection.

    Arguments:
        - msg: message
        - conn:  # ATTENTION, CE N EST PAS COMPLETË ICI # ATTENTION, CE N EST PAS COMPLETË ICI # ATTENTION, CE N EST PAS COMPLETË ICI # ATTENTION, CE N EST PAS COMPLETË ICI
    """

    # Encode the message
    message = msg.encode(FORMAT)
    # Get the length of the message
    msg_length = len(message)
    # Encode the length of the message
    send_length = str(msg_length).encode(FORMAT)
    # Add spaces to the length of the message to make it 64 characters long
    send_length += b' ' * (HEADERLEN - len(send_length))
    # Send the type of message
    conn.send(bytes(MSG, FORMAT))
    # Send the length of the message
    conn.send(send_length)
    # Send the message
    conn.send(message)


def sendMessageList(msg_list, conn):
    """
    Sends the whole list of messages to the specified connection.

    Arguments:
        - msg_list: list of all messages
        - conn: the connection to which the messages are sent
    """

    # Get length of list
    list_length = len(msg_list)
    # Encode the length of the list
    send_list_length = str(list_length).encode(FORMAT)
    # Add spaces to the length of the list to make it 64 characters long
    send_list_length += b' ' * (HEADERLEN - len(send_list_length))
    # Send the type of message
    conn.send(bytes(MSGLIST, FORMAT))
    # Send the length of the list
    conn.send(send_list_length)
    # Send the list
    for login, msg in msg_list:
        sendMessage(login, conn)
        sendMessage(msg, conn)


def saveMessageList(msg_list):
    """
    Saves the list of messages to a file named after
    the users in the conversation.

    Argument:
        - msg_list: list of all messages
    """

    # Get the users in the conversation
    users = [login for login in client_list.values()]
    users.sort()  # Sort the users alphabetically

    # Save the messages in a file, with the name of the file
    # being the users in the conversation for easy access
    with open(f"{'-'.join(users)}.txt", "w") as f:
        for login, msg in msg_list:
            f.write(f"{login}[:::]{msg}\n")


def loadMessageList(users):
    """
    Loads the list of messages from a file based on
    the users in the conversation.

    Argument:
        - users: name of all users
    """
    # Check if the file exists
    if not os.path.isfile(f"{'-'.join(users)}.txt"):
        return []
    # Load the messages from the file
    with open(f"{'-'.join(users)}.txt", "r") as f:
        msg_list = []
        for line in f.readlines():
            login, msg = line.split("[:::]")
            msg_list.append([login, msg.strip()])
        return msg_list


def handleClient(conn, addr):
    """
    Handles communication with a connected client, managing message exchange

    Arguments:
        - conn:  The connection that was established with the client
        - addr:  The connection's local address
    Return:
        - None: just exit the function
    """
    global client_list
    global message_list
    # Check if the client is permanent (not just a connection test)
    if conn.recv(HEADERLEN).decode(FORMAT) != "PERMANENT":
        conn.close()
        return
    print(f"[NEW CONNECTION] {addr} connected.")

    # Send data to the client (Data is sent under the form of bytes,
    # so we need to encode it (using utf-8))
    conn.send(bytes(f"Connected to the server {ADDR}", FORMAT))

    # Get the client's login
    login = conn.recv(128).decode(FORMAT)
    # Add the client to the list of clients
    client_list[conn] = login

    print(f"[ACTIVE CONNECTIONS] {len(client_list)}")

    # When the 2nd user connects to the server, load the messages from the file
    if len(client_list) > 1:
        users = [login for login in client_list.values()]
        users.sort()
        message_list = loadMessageList(users)
        if message_list:
            for conn in client_list.keys():
                sendMessage("LoadChatFile", conn)
                sendMessageList(message_list, conn)

    while True:
        try:
            # Receive length of the message from the client
            msg_length = conn.recv(HEADERLEN).decode(FORMAT)
            if msg_length:
                # Receive data from the client
                msg = conn.recv(int(msg_length)).decode(FORMAT)

                # If the client sends the DISCONNECT_MESSAGE,
                # disconnect the client
                if msg == DISCONNECT_MESSAGE:
                    break

                # If client uses command don't save the command
                if msg[0] == "/":
                    return

                # Add the message to the list of messages
                message_list.append([login, msg])
                # If there are more than 1 client, save the messages in a file
                if len(client_list) > 1:
                    saveMessageList(message_list)
                # Send the message to all the clients
                for client in client_list.keys():
                    sendMessageList(message_list, client)
        except:
            break

    # When out of while loop disconnect client
    print(f"[DISCONNECTED] {addr} disconnected.")
    del client_list[conn]
    conn.close()


def start():
    """
    Starts the server, listens for incoming connections, and handles each.
    """
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # Accept the connection from the client
        conn, address = server.accept()
        # Create a thread for each client (to handle multiple clients)
        thread = threading.Thread(target=handleClient, args=(conn, address))
        thread.start()


print("[STARTING] Server is starting...")
start()
