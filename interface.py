"""
Code for the WhatsDown application interface
Created on Tue Oct 23 19:44:37 1947
@author: H, R
"""
import os.path  # Needed for .exe compilation
import sys  # Needed for .exe compilation
import tkinter as tk
from tkinter import ttk, Tk, Scrollbar
from PIL import Image, ImageTk
from datetime import datetime  # To add the time of the message
import time

from datetime import datetime  # On peut ajouter l'heure de l'envoi du message
import math

def get_path(filename):
    """
    https://stackoverflow.com/questions/31836104/
    pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
    get_path() Imported from link above, needed in order to use
    images for the standalone .exe

    Returns the path for the given filename, considering .exe compilation.

    Args:
    - filename (str): The name of the file.

    Returns:
    - str: The path of the file.
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename


class WhatsDownMainWindow:
    """
    We create the main chat window on which the messages will be displayed.

    Attributes:
    - messages: List to store chat messages.
    - background_image: PhotoImage object for the background.
    - colorMe: Color code for messages sent by the local client.
    - colorOther: Color code for messages sent by other clients.
    - colorWarning: Color code for warning messages.
    - colorError: Color code for error messages.
    - text_color: Color code for text.
    - localClient: Instance of the local client.
    - screen_width: Width of the main window.
    - screen_height: Height of the main window.
    - input_box_height: Height of the input box.
    - button_size: Size of the send button.
    - title: Title of the main window.
    - root: Tkinter root window.
    - canvas: Canvas to hold the chat window.
    - scrollbar: Scrollbar for the chat window.
    - canvas_frame: Frame inside the canvas for displaying messages.

    Methods:
    - __init__: Initializes the main window and sets up its components.
    - on_close: Safely disconnects the client and closes the program.
    - on_enter_press: Handles the event when the Enter key is pressed.
    - scroll: Updates the scrollbar and adjusts the scrolls the canvas.
    - check_new_message: Checks for new messages at regular intervals.
    - handle_input: Sends the input text to the server, handles commands
    and clears the input box.
    - display_message: Displays a message in the chat window with
    appropriate formatting.
    - display_message_list: Displays a list of messages in the chat window.
    - fibonacci: Calculates the nth Fibonacci number recursively.
    - chr_to_pixel: Converts char length to pixels. Not used for now
    because resize deactivated => no need for calculations.
    """
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, LOCALCLIENT):
        """
        Creates the main application window.

        Args:
        - WINDOW_WIDTH: Width of the main window.
        - WINDOW_HEIGHT: Height of the main window.
        - LOCALCLIENT: Instance of the local client.
        """
        # Initialize the variables
        self.messages = []
        self.background_image = None
        self.colorMe = "lightgreen"
        self.colorOther = "lightblue"
        self.colorWarning = "yellow"
        self.colorError = "red"
        self.text_color = "black"
        self.localClient = LOCALCLIENT

        # Set window width and height
        self.screen_width = WINDOW_WIDTH
        self.screen_height = WINDOW_HEIGHT

        self.input_box_height = 40  # Set input box height

        self.button_size = self.input_box_height  # Set the send button size

        # Set window title
        self.title = f"Whatsdown! Logged in as: {self.localClient.login}"

        # Create the main application window
        self.root = Tk()

        # Set window size and open the window in the center of the screen
        self.root.geometry(
            f"{self.screen_width}x{self.screen_height}+"
            f"{int(self.root.winfo_screenwidth() / 2 - self.screen_width / 2)}+{0}")

        # Set window title and icon
        self.root.title(self.title)
        self.root.iconbitmap(get_path("icon.ico"))

        # If we don't put everything in one common frame, the display is messed up
        self.hold_all_in_one_frame = ttk.Frame(self.root, height=self.screen_height)
        self.hold_all_in_one_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas to hold the chat window
        self.canvas = tk.Canvas(self.hold_all_in_one_frame, height=self.screen_height)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbar for when many messages go out of the screen
        self.scrollbar = Scrollbar(self.canvas, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.canvas_frame = ttk.Frame(self.canvas, style="Message.TFrame")
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        # To adapt the scroll bar to the canvas when size changed
        self.canvas.bind('<Configure>', self.canvas.config(scrollregion=self.canvas.bbox("all")))

        # Add the input box
        shift = self.input_box_height

        self.input_box = tk.Entry(self.root, width=WINDOW_WIDTH // 10 - shift // 8, bg="white", fg="black",
                                  font=("Comic Sans MS", 12), borderwidth=2, relief="sunken")
        self.input_box.pack(side=tk.LEFT)
        self.input_box.bind('<Return>', self.on_enter_press)

        # Add the send button and display it
        send_icon = ImageTk.PhotoImage(
            Image.open(get_path("send_icon.png")).resize(
                (int(self.button_size * 0.8), int(self.button_size * 1)),
                Image.BOX))  # Take the image and resize it

        self.send_button = tk.Button(self.root, height=int(self.button_size * 0.8),
                                     width=int(self.button_size * 1),
                                     text='Click Me !',
                                     image=send_icon, command=lambda: self.handle_input())

        self.send_button.pack(side=tk.LEFT)

        self.messages = []

        self.check_new_message()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.scroll()

        # for i in range(20):
        #     self.displayMessage(i, "Hi", self.canvas_frame)
        self.canvas.yview_moveto(1.0)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.resizable(False, False)
        self.root.mainloop()

    # Called when pressing the "X" to close the window
    # Safely disconnects the client and ends the program
    def on_close(self):
        self.localClient.send(self.localClient.DISCONNECT_MESSAGE)
        self.localClient.connected = False
        self.localClient.client.close()
        self.root.destroy()
        quit()

    def on_enter_press(self, event):
        """
        Activates when enter pressed to send the message.

        """
        self.handle_input()

    def scroll(self):
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)

    def check_new_message(self):
        # Check if the chat file was found and loaded
        if self.localClient.loadChatFile and self.localClient.newMessage:
            self.display_message_list()
            self.localClient.loadChatFile = False
            self.localClient.newMessage = False

        # Check if there are new messages
        if self.localClient.newMessage:
            # Display the messages
            self.display_message(self.localClient.message_list[-1][1], self.localClient.message_list[-1][0])
            self.localClient.newMessage = False

        # Check again in 100ms
        self.root.after(100, self.check_new_message)

    # Handles the input
    def handle_input(self):
        """
        Sends the input text to the server and doesn't display it.
        Doesn't send the input text if it's empty.
        """
        input_text = self.input_box.get()  # Get input
        self.input_box.delete("0", tk.END)  # Clear input from beginning to end

        # Don't send if message is empty
        if input_text == "" or input_text == " ":
            return

        # Check if message is a command
        if input_text[0] == "/":
            arguments = input_text.split()

            # Disconnect client if client send the disconnect message
            if input_text == self.localClient.DISCONNECT_MESSAGE:
                self.on_close()

            # Send the fibonacci sequence
            elif input_text.startswith("/fibonacci"):
                # Handle case where user doesn't provide arguments
                if len(arguments) < 2:
                    self.display_message(arguments[0] + " requires 1 argument (int)!", "Error")
                    return

                # Handle case where user doesn't provide an integer
                try:
                    n = int(arguments[1])
                except ValueError:
                    self.display_message(arguments[0] + " requires an integer as an argument!", "Error")
                    return

                # Handle case where user inputs invalid integer (less than 1)
                if n < 0:
                    self.display_message(arguments[0] + " requires a positive integer !", "Error")
                    return
                # Handle case where user inputs a too big integer
                if n>30:
                    self.display_message(arguments[0] + " requires an integer smaller than 31 !", "Warning")
                    return

                self.localClient.send(f"The fibonacci number {n} is: {self.fibonacci(n)}")

            else:
                self.display_message(arguments[0] + " | Command not found!", "Error")
                return

        # If not a command send the message directly
        else:
            self.localClient.send(input_text)

    # Do we need the "where" argument since it's always the same?
    def display_message(self, message, who):
        frame = ttk.Frame(self.canvas_frame)
        sender = ttk.Label(frame, text=f"{who} says:", font=("Comic Sans MS", 8, "italic"))
        sender.grid(column=0, row=0, sticky="w")
        color = self.colorOther

        if who == self.localClient.login:
            color = self.colorMe
        elif who == "Error":
            color = self.colorError
        elif who == "Warning":
            color = self.colorWarning

        desired_height = math.ceil(len(message) / 56)

        message_text = tk.Text(frame, wrap=tk.WORD, width=int(self.screen_width / 8.3),
                               height=desired_height, bg=color)

        message_text.insert(tk.END, f"{message}")
        message_text.config(state=tk.DISABLED)  # A comprendre?
        message_text.grid(column=0, row=1, sticky="w")
        frame.grid(column=0, row=self.canvas_frame.grid_size()[1], sticky="w")
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        self.scroll()

    def display_message_list(self):
        """
        Affiche la liste des messages dans la fenêtre.
        """
        # Prend la liste de messages du serveur
        messages = self.localClient.message_list
        # Affiche les messages un par un
        for login, msg in messages:
            self.display_message(msg, login)

    def fibonacci(self, n):
        """
        Calcule le n-ième nombre de Fibonacci récursivement.
        """
        if n == 0 or n == 1:
            return n

        return self.fibonacci(n - 1) + self.fibonacci(n - 2)


    def chr_to_pixel(self, char):
        """
        Converts char length to pixels
        """
        return ord(char) * 8


class WhatsDownLoginPage:
    def __init__(self, SIZEX, SIZEY):
        """
        Crée la page de connexion de l'application.
        """
        self.root = Tk()
        self.root.geometry(f"{SIZEX}x{SIZEY}")
        self.root.title("WhatsDown! - Login")
        self.root.iconbitmap("icon.ico")

        self.login = ""

        self.root.mainloop()

    def get_login(self):
        """
        Renvoie le nom d'utilisateur saisi.
        """
        return self.login
