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

        self.input_box_height = 40

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

        # Set frame to add buttons
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Create a canvas to hold the chat window
        self.canvas = tk.Canvas(self.frame, width=self.screen_width,
                                height=(self.screen_height - self.input_box_height))
        self.canvas.pack()

        self.chat_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.chat_frame, anchor=tk.NW)

        # Set background image with background() function
        self.setBg()

        # Add scrollbar for when many messages go out of the screen
        self.scrollbar = Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Create a frame for the chat messages
        self.chat_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.chat_frame, anchor=tk.NW, width=self.screen_width,height=self.screen_height - self.input_box_height)

        # Add the input box
        shift = self.input_box_height
        self.input_box = tk.Entry(self.root, width=self.screen_width - shift, bg="white", fg="black",
                                  font=("Comic Sans MS", 12), borderwidth=2, relief="sunken")
        self.input_box.place(x=(self.screen_width // 2), y=self.screen_height, height=100,
                             width=self.screen_width - 400)
        self.input_box.place(x=0, y=self.root.winfo_height() - self.input_box_height,
                             height=self.input_box_height, width=self.root.winfo_width())

        # Add the send button and display it
        self.button_size = self.input_box_height
        send_icon = ImageTk.PhotoImage(Image.open("send_icon.png").resize((self.button_size, self.button_size),
                                                                          Image.BOX))  # I didn't put self

        self.send_button = tk.Button(self.root, height=self.button_size, width=self.button_size, text='Click Me !',
                                     image=send_icon, border="0", command=self.envoyer_texte)
        self.send_button.place(x=int(self.screen_width - self.button_size),
                               y=int(self.screen_height - self.button_size))
        # self.send_button.place(x=(self.screen_width-self.button_size), y=(self.screen_height-self.button_size))

        self.messages = []

        self.root.resizable(width=False, height=False)

        self.root.mainloop()

    def setBg(self):
        """"
        Adds background image to the main application window
        """
        # self.background_image = tk.PhotoImage(file="background.png")
        self.background_image = Image.open("background.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.canvas, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

    # Take the input and move everything up
    def envoyer_texte(self):
        """
        Sends the input text to the server and doesn't display it.
        Doesn't send the input text if it's empty.
        """
        self.input_text = self.input_box.get()  # Get input
        client.send(self.input_text)
        # print(self.input_text)
        if self.input_text.replace(" ", ""):
            self.messages.append((self.input_text, client.login))
            print(self.messages)
            self.display_messages()
        self.input_box.delete("0", tk.END)  # Clear input

    def display_messages(self):
        for i, (message, who) in enumerate(self.messages):
            print(i, message, who)
            color = "lightgreen"
            self.chat_frame.image = self.background_image
            # put box in which there will be text message label
            message_frame = tk.Frame(self.chat_frame, padx=5, pady=5, bg=color, bd=2, relief=tk.GROOVE)

            message_frame.grid(row=i, column=1, sticky=tk.W, padx=10, pady=5)
            message_frame.image = self.background_image
            message_label = tk.Label(message_frame, text=message, wraplength=self.screen_width, justify=tk.RIGHT,
                                     bg=color)
            message_label.pack(anchor=tk.SE)

            # self.chat_frame.update_idletasks()
            # self.canvas.config(scrollregion=self.canvas.bbox("all"))


if __name__ == '__main__':
    try:
        interface = Interface(480, 920, "Very Safe Messaging App!")
    except Exception as e:
        print(f"{e} [EXCEPTION] occured")
        sys.exit()

# def create_rounded_frame(canvas, x, y, width, height, corner_radius, fill_color):
#     canvas.create_arc(x, y, x + 2*corner_radius, y + 2*corner_radius, start=90, extent=90, fill=fill_color)
#     canvas.create_arc(x + width - 2*corner_radius, y, x + width, y + 2*corner_radius, start=0, extent=90, fill=fill_color)
#     canvas.create_arc(x, y + height - 2*corner_radius, x + 2*corner_radius, y + height, start=180, extent=90, fill=fill_color)
#     canvas.create_arc(x + width - 2*corner_radius, y + height - 2*corner_radius, x + width, y + height, start=270, extent=90, fill=fill_color)
#     canvas.create_rectangle(x + corner_radius, y, x + width - corner_radius, y + height, fill=fill_color)
#     canvas.create_rectangle(x, y + corner_radius, x + width, y + height - corner_radius, fill=fill_color)
# create_rounded_frame(canvas, 50, 50, 200, 100, 20, "lightblue")
