# encode: utf-8
"""
Created on 4/10/23 13:00

@author: H, R
"""
import tkinter as tk
from tkinter import ttk, Tk, Entry

from PIL import Image, ImageTk


class Interface:
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, TITLE):
        """"
        Creates the main application window
        """
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

        # Set background image with background() function
        self.setBackground()

        # Set frame to add buttons
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Add the input box
        self.input_box = tk.Entry(self.root, width=self.screen_width, bg="white", fg="black",
                                  font=("Comic Sans MS", 12), borderwidth=2, relief="sunken")
        self.input_box.place(x=(self.screen_width // 2), y=self.screen_height, height=100,
                             width=self.screen_width - 400)

        self.input_box.place(x=0, y=self.root.winfo_height() - self.input_box_height,
                             height=self.input_box_height, width=self.root.winfo_width())

        # Add the send button and display it
        self.button_size = self.input_box_height
        send_icon = ImageTk.PhotoImage(Image.open("send_icon.png").resize((self.button_size, self.button_size),
                                                                          Image.BOX))  # I didn't put self.
        self.send_button = tk.Button(self.root, height=self.button_size, width=self.button_size, text='Click Me !',
                                     image=send_icon, border="0").place(x=int(self.screen_width - self.button_size),
                                                            y=int(self.screen_height - self.button_size))
        # self.send_button.place(x=(self.screen_width-self.button_size), y=(self.screen_height-self.button_size))

        # self.send_button

        self.root.resizable(width=False, height=False)

        self.root.mainloop()

    def setBackground(self):
        """"
        Adds background image to the main application window
        """
        self.background_image = Image.open("background.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)


if __name__ == '__main__':
    interface = Interface(480, 920, "Very Safe Messaging App!")
