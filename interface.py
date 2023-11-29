"""
This class represents the main window of the WhatsDown application.

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
    - onEnterPress: Handles the event when the Enter key is pressed.
    - scroll: Updates the scrollbar and adjusts the scrolls the canvas.
    - checkNewMessage: Checks for new messages at regular intervals.
    - handleInput: Sends the input text to the server, handles commands and clears the input box.
    - displayMessage: Displays a message in the chat window with appropriate formatting.
    - displayMessageList: Displays a list of messages in the chat window.
    - Fibonacci: Calculates the nth Fibonacci number recursively.

"""

import os.path  # Needed for .exe compilation
import sys  # Needed for .exe compilation
import tkinter as tk
from tkinter import ttk, Tk, Scrollbar
from PIL import Image, ImageTk
from datetime import datetime  # On peut ajouter l'heure de l'envoi du message


# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
# get_path() Imported from link above, needed in order to use images for the standalone .exe
def get_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return filename


class WhatsDownMainWindow:
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, LOCALCLIENT):
        """"
        Creates the main application window
        """
        # Initialize variables
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

        # Set input box height
        self.input_box_height = 40

        self.button_size = self.input_box_height

        # Set window title
        self.title = f"Whatsdown! Logged in as: {self.localClient.login}"

        # Create the main application window
        self.root = Tk()

        # Set window size and Open the window in the center of the screen
        self.root.geometry(
            f"{self.screen_width}x{self.screen_height}+{int(self.root.winfo_screenwidth() / 2 - self.screen_width / 2)}+{0}")  # !!! + THAN 80 CHR.
        # Set window title and icon
        self.root.title(self.title)
        self.root.iconbitmap(get_path("icon.ico"))

        self.background_image = tk.PhotoImage(file=get_path("background.png"))

        # Background to be added to message frame not canvas
        self.messages_frame = ttk.Frame(self.root, style="Message.TFrame", height=300)
        self.messages_frame.pack(fill=tk.BOTH, expand=True)

        # Add a label to the frame to display the background image
        background_label = ttk.Label(self.messages_frame, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        # Create a canvas to hold the chat window
        self.canvas = tk.Canvas(self.messages_frame, highlightthickness=0, height=self.screen_height)
        # self.canvas.create_image(0, self.screen_height-self.background_image.height()-self.input_box_height, anchor=tk.NW, image=self.background_image)
        # tk.LEFT au cas ou on veut mettre des boutons a droite dans de prochaines versions
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # self.canvas.create_window((0, 0), window=self.canvas, anchor=tk.NW)

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

        # self.input_box.place(x=0, y=self.root.winfo_height() - self.input_box_height,
        #                      height=self.input_box_height, width=self.root.winfo_width() - self.button_size)
        self.input_box.pack(side=tk.LEFT)
        self.input_box.bind('<Return>', self.onEnterPress)

        # Add the send button and display it
        send_icon = ImageTk.PhotoImage(
            Image.open(get_path("send_icon.png")).resize((int(self.button_size * 0.8), int(self.button_size * 1)),
                                                         Image.BOX))  # I didn't put self

        self.send_button = tk.Button(self.root, height=int(self.button_size * 0.8), width=int(self.button_size * 1),
                                     text='Click Me !',
                                     image=send_icon, command=lambda: self.handleInput())

        self.send_button.pack(side=tk.LEFT)
        # self.send_button.place(x=(self.screen_width-self.button_size), y=(self.screen_height-self.button_size))

        self.messages = []

        # self.root.resizable(width=False, height=False)

        self.checkNewMessage()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.scroll()

        # for i in range(20):
        #     self.displayMessage(i, "Hi", self.canvas_frame)
        self.canvas.yview_moveto(1.0)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.mainloop()

    # Called when pressing the "X" to close the window
    # Safely disconnects the client and ends the program
    def on_close(self):
        self.localClient.send(self.localClient.DISCONNECT_MESSAGE)
        self.localClient.connected = False
        self.localClient.client.close()
        self.root.destroy()
        quit()

    def onEnterPress(self, event):
        self.handleInput()

    def scroll(self):
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)

    def checkNewMessage(self):
        # Check if the chat file was found and loaded
        if self.localClient.loadChatFile and self.localClient.newMessage:
            self.displayMessageList()
            self.localClient.loadChatFile = False
            self.localClient.newMessage = False

        # Check if there are new messages
        if self.localClient.newMessage:
            # Display the messages
            self.displayMessage(self.localClient.message_list[-1][1], self.localClient.message_list[-1][0])
            self.localClient.newMessage = False

        # Check again in 100ms
        self.root.after(100, self.checkNewMessage)

    # Handles the input
    def handleInput(self):
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
                    self.displayMessage(arguments[0] + " requires 1 argument (int)!", "Error")
                    return

                # Handle case where user doesn't provide an integer
                try:
                    n = int(arguments[1])
                except ValueError:
                    self.displayMessage(arguments[0] + " requires an integer as an argument!", "Error")
                    return

                # Handle case where user inputs invalid integer (less than 1)
                if n < 1:
                    self.displayMessage(arguments[0] + " requires an integer greater than 1!", "Error")
                    return

                if n > 30:
                    self.displayMessage(arguments[0] + " should not be larger than 30!", "Warning")

                self.localClient.send(f"{n}th fibonacci number is: {self.Fibonacci(n)}")

            else:
                self.displayMessage(arguments[0] + " | Command not found!", "Error")
                return

        # If not a command send the message directly
        else:
            self.localClient.send(input_text)

    # Do we need the "where" argument since it's always the same?
    def displayMessage(self, message, who):
        frame = ttk.Frame(self.canvas_frame)
        now = datetime.now().strftime("%H:%M:%S")
        sender = ttk.Label(frame, text=f"{who}, sent at {now}", font=("Comic Sans MS", 8, "italic"))
        sender.grid(column=0, row=0, sticky="w")
        color = self.colorOther

        # if who == self.localClient.login:
        #     ###!!! Y A ENCORE A REFORMATER LE HEIGHT POUR ADAPTER A LA TAILLE DU TEXTE
        #     message_text = tk.Text(frame, wrap=tk.WORD, width=int(self.screen_width / 8.3), height=1, bg=self.colorMe)
        # else:
        #     message_text = tk.Text(frame, wrap=tk.WORD, width=int(self.screen_width / 8.3), height=1, bg=self.colorOther)

        if who == self.localClient.login:
            color = self.colorMe
        elif who == "Error":
            color = self.colorError
        elif who == "Warning":
            color = self.colorWarning

        message_text = tk.Text(frame, wrap=tk.WORD, width=int(self.screen_width / 8.3), height=1, bg=color)

        message_text.insert(tk.END, f"{message}")
        message_text.config(state=tk.DISABLED)  # A comprendre?
        message_text.grid(column=0, row=1, sticky="w")
        frame.grid(column=0, row=self.canvas_frame.grid_size()[1], sticky="w")
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        self.scroll()

    def displayMessageList(self):
        # Get the messages from the server
        messages = self.localClient.message_list
        # Display the messages
        for login, msg in messages:
            self.displayMessage(msg, login)

    def Fibonacci(self, n):
        if n == 0 or n == 1:
            return n

        return self.Fibonacci(n - 1) + self.Fibonacci(n - 2)


class WhatsDownLoginPage:
    def __init__(self, SIZEX, SIZEY):
        self.root = Tk()
        self.root.geometry(f"{SIZEX}x{SIZEY}")
        self.root.title("WhatsDown! - Login")
        self.root.iconbitmap("icon.ico")

        self.login = ""

        self.root.mainloop()

    def getLogin(self):
        return self.login
