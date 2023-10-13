# encode: utf-8
"""
Created on 4/10/23 13:00

@author: H, R
"""
import tkinter as tk
from tkinter import ttk, Tk, Entry, Scrollbar
import sys
from PIL import Image, ImageTk
import client


# !!! Work with CANVAS
class Interface:
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, TITLE):
        """"
        Creates the main application window
        """
        # Initialize variables
        self.input_text = None
        self.background_label = None
        self.background_image = None
        self.background_photo = None

        # Set window width and height
        self.screen_width = WINDOW_WIDTH
        self.screen_height = WINDOW_HEIGHT

        # Set input box height
        self.input_box_height = 40

        self.button_size = self.input_box_height

        # Set window title
        self.title = TITLE

        # Create the main application window
        self.root = Tk()

        # Set window size and Open the window in the center of the screen
        self.root.geometry(
            f"{self.screen_width}x{self.screen_height}+{int(self.root.winfo_screenwidth() / 2 - self.screen_width / 2)}+{0}")  # !!! + THAN 80 CHR.
        # Set window title and icon
        self.root.title(self.title)
        self.root.iconbitmap("icon.ico")

        self.background_image = tk.PhotoImage(file="background.png")

        # Create a canvas to hold the chat window
        self.canvas = tk.Canvas(self.root, width=self.screen_width,
                                height=(self.screen_height - self.input_box_height))

        self.canvas.create_image(0, self.screen_height-self.background_image.height()-self.input_box_height, anchor=tk.NW, image=self.background_image)

        self.canvas.pack(fill=tk.BOTH, expand=True)

        # self.canvas.create_window((0, 0), window=self.canvas, anchor=tk.NW)

        # Add scrollbar for when many messages go out of the screen
        self.scrollbar = Scrollbar(self.canvas, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Add the input box
        shift = self.input_box_height
        self.input_box = tk.Entry(self.root, width=self.screen_width - shift, bg="white", fg="black",
                                  font=("Comic Sans MS", 12), borderwidth=2, relief="sunken")

        self.input_box.place(x=0, y=self.root.winfo_height() - self.input_box_height,
                             height=self.input_box_height, width=self.root.winfo_width() - self.button_size)

        # Add the send button and display it
        send_icon = ImageTk.PhotoImage(Image.open("send_icon.png").resize((self.button_size, self.button_size),
                                                                          Image.BOX))  # I didn't put self

        self.send_button = tk.Button(self.root, height=self.button_size, width=self.button_size, text='Click Me !',
                                     image=send_icon, border="0", command=self.envoyer_texte)

        self.send_button.place(x=(self.screen_width-self.button_size), y=(self.screen_height-self.button_size))

        self.messages = []

        self.root.resizable(width=False, height=False)

        self.root.mainloop()

    # Take the input and move everything up
    def envoyer_texte(self):
        """
        Sends the input text to the server and doesn't display it.
        Doesn't send the input text if it's empty.
        """
        self.input_text = self.input_box.get()  # Get input
        localClient.send(self.input_text)
        # print(self.input_text)
        if self.input_text.replace(" ", ""):
            self.messages.append((self.input_text, localClient.login))
            print(self.messages)
            self.display_messages()
        self.input_box.delete("0", tk.END)  # Clear input from beginning to end

    def display_messages(self):
        # for i, (message, who) in enumerate(self.messages):
        message, who = self.messages[-1]
        color = "lightgreen"
        text_color = "black"

        # put box in which there will be text message label
        message_frame = tk.Frame(self.canvas, bg=color) #, relief=tk.GROOVE)
        message_frame.pack(padx=5, pady=5, anchor=tk.NW)

        message_label = tk.Label(message_frame, text=f"{who}: {message}", wraplength=self.screen_width//2, justify=tk.LEFT,
                                 bg=color, fg=text_color)
        message_label.pack(padx=5, pady=5)


if __name__ == '__main__':
    localClient = client.Client()
    try:
        print("init")
        interface = Interface(480, 920, f"Whatsdown! Logged in as: {localClient.login}")
    except Exception as e:
        print(f"[EXCEPTION] {e} occurred")
        sys.exit()