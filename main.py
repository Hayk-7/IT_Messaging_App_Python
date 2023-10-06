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
        self.title = TITLE

        # Create the main application window
        self.root = Tk()

        # Set window size
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")

        # Set window title and icon
        self.root.title(self.title)
        self.root.iconbitmap("icon.ico")

        # Set background image with background() function
        self.setBackground()

        # Set frame to add buttons
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Add the input box
        self.input_box = tk.Entry(self.root, width=50, font=("Arial", 12), borderwidth=2, relief="sunken")
        self.input_box.pack(pady=40, side="bottom")
        # self.input_box.place(x=WINDOW_WIDTH/2-100, y=WINDOW_HEIGHT/2-100)

        # Add the send button
        # self.send_button = tk.Button(self.root, text="Send", font=("Arial", 12), borderwidth=2, relief="raised")
        # self.send_button.pack(pady=40, side="bottom")

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
    interface = Interface(512, 1024, "Very Safe Messaging App!")
