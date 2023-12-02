"""
Code for the WhatsDown application interface.

Created on Tue Oct 23 19:44:37 1947
@author: H, R
"""
import os.path  # Needed for .exe compilation
import sys  # Needed for .exe compilation
import tkinter as tk
import math
from tkinter import Tk, Scrollbar
from PIL import Image, ImageTk


def get_path(filename):
    """
    https://stackoverflow.com/questions/31836104/
    pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
    get_path() imported from link above, needed in order to use
    images for the standalone .exe

    Return the path for the given filename, considering .exe compilation.

    Args:
    - filename (str): The name of the file.

    Returns:
    - str: The path of the file.
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return filename


class WhatsDownMainWindow:
    """
    We create the main chat window on which the messages will be displayed.

    Attributes:
    - messages: List to store chat messages.
    - background_image: PhotoImage object for the background.
    - color_me: Color code for messages sent by the local client.
    - color_other: Color code for messages sent by other clients.
    - color_warning: Color code for warning messages.
    - color_error: Color code for error messages.
    - text_color: Color code for text.
    - local_client: Instance of the local client.
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
    """

    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, LOCAL_CLIENT):
        """
        Create the main application window.

        Args:
        - WINDOW_WIDTH: Width of the main window.
        - WINDOW_HEIGHT: Height of the main window.
        - LOCAL_CLIENT: Instance of the local client.
        """
        # Initialize the variables
        self.messages = []
        self.background_image = None
        self.color_me = "lightgreen"
        self.color_other = "lightblue"
        self.color_warning = "yellow"
        self.color_error = "red"
        self.text_color = "black"
        self.local_client = LOCAL_CLIENT

        # Set window width and height
        self.screen_width = WINDOW_WIDTH
        self.screen_height = WINDOW_HEIGHT

        self.input_box_height = 40  # Set input box height

        self.button_size = self.input_box_height  # Set the send button size

        # Set window title
        self.title = f"Whatsdown! Logged in as: {self.local_client.login}"

        # Create the main application window
        self.root = Tk()

        # Set window size and open the window in the center of the screen
        self.root.geometry(
            f"{self.screen_width}x{self.screen_height}+"
            f"{int(self.root.winfo_screenwidth() / 2 - self.screen_width / 2)}"
            f"+{0}")

        # Set window title and icon
        self.root.title(self.title)
        self.root.iconbitmap(get_path("icon.ico"))

        # If we don't put everything in one common frame,
        # the display is messed up
        self.hold_all_in_one_frame = tk.Frame(self.root,
                                              height=self.screen_height)
        # Show the frame
        self.hold_all_in_one_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas to hold the chat window
        self.canvas = tk.Canvas(self.hold_all_in_one_frame,
                                height=self.screen_height)
        # Show the canvas on the previous frame
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbar for when many messages go out of the screen
        # Scrollbar design
        self.scrollbar = Scrollbar(self.canvas, orient=tk.VERTICAL,
                                   command=self.canvas.yview)
        # Show the scrollbar
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Allows the scrollbar to scroll the canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas to display the messages
        # We are not allowed to add window on canvas directly
        self.canvas_frame = tk.Frame(self.canvas)

        # This is the window which on which everything will be displayed
        # A window has to be on a frame, not a canvas.
        # It allows us to make the elements on it part of the canvas
        # It means that the scrollbar will move everything.
        self.canvas.create_window((0, 0), window=self.canvas_frame,
                                  anchor="nw")

        # Knows the shift to apply to the input box from the right
        shift = self.input_box_height

        # Create the input box and calculate its coordinates
        self.input_box = tk.Entry(self.root,
                                  width=WINDOW_WIDTH // 10 - shift // 8,
                                  bg="white", fg="black",
                                  font=("Comic Sans MS", 12),
                                  borderwidth=2, relief="sunken")
        # Show the input box
        self.input_box.pack(side=tk.LEFT)
        # Adds the event listener for when the user presses enter
        self.input_box.bind('<Return>', self.on_enter_press)

        # Import the send button and resize it
        send_icon = ImageTk.PhotoImage(
            Image.open(get_path("send_icon.png")).resize(
                (int(self.button_size * 0.8), int(self.button_size * 1))))
        # Create the send button and add the image on it
        self.send_button = tk.Button(self.root,
                                     height=int(self.button_size * 0.8),
                                     width=int(self.button_size * 1),
                                     image=send_icon,
                                     command=lambda: self.handle_input())
        # Show the send button
        self.send_button.pack(side=tk.LEFT)

        self.check_new_message()  # Check for new messages
        # Configure the scroll region => the scroll bar will be updated
        # when new messages are added
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.scroll()  # Scroll to the bottom of the canvas in the beginning

        # Add the event listener for when the user closes the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Set the window to not be resizable
        self.root.resizable(False, False)
        # Makes the code wait for events until we close the window
        self.root.mainloop()

    def on_close(self):
        """
        Called when pressing the "X" to close the window.

        Safely disconnects the client and ends the program.
        """
        try:
            # Sends the message to disconnect the client from server
            self.local_client.send(self.local_client.DISCONNECT_MESSAGE)
        except:
            pass
        self.local_client.connected = False
        self.local_client.client.close()
        self.root.destroy()  # To close the window
        quit()

    def on_enter_press(self, event):
        """
        Activates when enter pressed to send the message.

        Argument:
            - event: not needed, but by default, the listener
            sends the key which has been pressed
        """
        self.handle_input()

    def scroll(self):
        """
        Update the scrollbar and scrolls the canvas to the bottom
        when new message sent.

        To function correctly, we have to update idletasks() before
        and after the config() method.
        """
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)  # Move the scrollbar to the bottom

    def check_new_message(self):
        """
        If the chat file was found, display the messages.
        If there are new messages, display them.

        This function repeats itself every 100ms.
        """
        # Check if the chat file exists
        if self.local_client.load_chat_file and self.local_client.newMessage:
            self.display_message_list()  # Displays the saved messages
            self.local_client.load_chat_file = False
            self.local_client.newMessage = False

        # Check if there are new messages
        if self.local_client.newMessage:
            # Display the last message from message_list
            # which is stored in localClient
            self.display_message(self.local_client.message_list[-1][1],
                                 self.local_client.message_list[-1][0])
            self.local_client.newMessage = False

        # Check again in 100ms
        self.root.after(100, self.check_new_message)

    # Handles the input
    def handle_input(self):
        """
        Send the input text to the server and doesn't display it.
        Doesn't send the input text if it's empty.

        Return:
            - None: to exit the function
        """
        # Get input in input box
        input_text = self.input_box.get()
        # Clear input from beginning to end
        self.input_box.delete("0", tk.END)

        # Don't send if the message content is empty
        if input_text in ("", " "):
            return

        # Check if the message is a command
        if input_text[0] == "/":
            arguments = input_text.split()

            # Disconnect client if client send the disconnect message
            if input_text == self.local_client.DISCONNECT_MESSAGE:
                self.on_close()

            # Send the fibonacci sequence
            elif input_text.startswith("/fibonacci"):
                # Handle case where user doesn't provide arguments
                if len(arguments) < 2:
                    self.display_message(arguments[0] +
                                         " requires 1 argument (int)!",
                                         "Error")
                    return

                # Handle case where user doesn't provide an integer
                try:
                    num = int(arguments[1])
                except ValueError:
                    self.display_message(arguments[0] +
                                         " requires an int as an argument !",
                                         "Error")
                    return

                # Handle case where user inputs invalid integer
                # (less than 1 or more than 30)
                if num < 0:
                    self.display_message(arguments[0] +
                                         " requires a positive integer !",
                                         "Error")
                    return
                # Handle case where user inputs a too big integer
                if num > 30:
                    self.display_message(arguments[0] +
                                         " requires an int smaller than 31 !",
                                         "Warning")
                    return

                self.local_client.send(f"The fibonacci number {num} is:"
                                       f"{self.fibonacci(num)}")

            else:  # If command not found, display error message
                self.display_message(arguments[0] + " | Command not found!",
                                     "Error")
                return

        # If not a command send the message directly
        else:
            self.local_client.send(input_text)

    # Do we need the "where" argument since it's always the same?
    def display_message(self, message, who):
        """
        Display a message in the chat window with appropriate formatting
        and color depending on who sent it.

        Arguments:
            - message: content
            - who: sender
        The message color is chosen according to who is the sender
        """
        # Creates the frame: the box which will contain all
        # the information of the message.
        frame = tk.Frame(self.canvas_frame)
        # Create a label in the frame to indicate sender's name
        sender = tk.Label(frame, text=f"{who} says:", font=("Comic Sans MS", 8, "italic"))
        # Place the name at the top of the frame
        sender.grid(column=0, row=0, sticky="w")
        # Color of message content background
        color = self.color_other

        if who == self.local_client.login:
            color = self.color_me
        elif who == "Error":
            color = self.color_error
        elif who == "Warning":
            color = self.color_warning

        # Calculate the height of the message (it is an approximation)
        desired_height = math.ceil(len(message) / 56)

        # Create the text box. We divide by 8.3 because screen_width
        # is in pixels but width not.
        message_text = tk.Text(frame, wrap=tk.WORD,
                               width=int(self.screen_width / 8.3),
                               height=desired_height, bg=color)

        # Add the message at the end of the text box
        message_text.insert(tk.END, f"{message}")
        #  We can't modify the text after it is sent
        message_text.config(state=tk.DISABLED)
        # To avoid overlapping sender's name, we set the row to 1.
        message_text.grid(column=0, row=1, sticky="w")
        # Place the frame in the grid layout, adjusting the row to
        # avoid overlap.
        # The row increments automatically.
        frame.grid(column=0, row=self.canvas_frame.grid_size()[1])

        # Scroll to the bottom of the canvas to see the new message
        self.scroll()

    def display_message_list(self):
        """Display all the messages in the message list at once."""
        # Get the list from server
        messages = self.local_client.message_list
        # Display the messages in order, one by one
        for login, msg in messages:
            self.display_message(msg, login)

    def fibonacci(self, num):
        """
        Calculate recursively the n-th number of
        the fibonacci sequence. It is a terminal recursion,
        therefore, we did a basic fibonacci function which
        takes too much time for n > 30.
        """
        if num in (0, 1):  # Initial case
            return num

        return self.fibonacci(num - 1) + self.fibonacci(num - 2)


class WhatsDownLoginPage:
    """
    This class is not in use yet.
    Pre-made for future, more sophisticated versions of the app.
    """

    def __init__(self, SIZE_X, SIZE_Y):
        """
        Crée la page de connexion de l'application avec
        les valeurs de défaut.
        """
        self.root = Tk()
        self.root.geometry(f"{SIZE_X}x{SIZE_Y}")
        self.root.title("WhatsDown! - Login")
        self.root.iconbitmap("icon.ico")

        self.login = ""

        self.root.mainloop()

    def get_login(self):
        """Send the username given in terminal."""
        return self.login
