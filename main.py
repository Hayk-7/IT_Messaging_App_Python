# encode: utf-8
"""
Created on 4/10/23 13:00

@author: H, R
"""
import tkinter as tk
from tkinter import ttk, Tk, Entry

from PIL import Image, ImageTk

class Interface:
    def __init__(self):
        """"
        Creates the main application window
        """
        # Set the constant size of the window
        WINDOW_WIDTH = 512
        WINDOW_HEIGHT = 1024

        self.root = Tk()
        self.root.geometry("290x400")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.title("WhatsDown")

        # Set background image with background() function
        self.background()

        # Set frame to add buttons
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # Add the input box
        self.input_box = tk.Entry(self.root, width=50, font=("Arial", 12), borderwidth=2, relief="sunken")
        self.input_box.pack(pady=40, side="bottom")
        # self.input_text = Entry(self.root, width=50)
        # self.input_text.pack()
        # self.input_text.place(x=WINDOW_WIDTH/2-100, y=WINDOW_HEIGHT/2-100)

        self.root.resizable(width=False, height=False)

        self.root.mainloop()


    def background(self):
        """"
        Adds background image to the main application window
        """
        self.background_image = Image.open("background.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

if __name__ == '__main__':
    interface = Interface()

