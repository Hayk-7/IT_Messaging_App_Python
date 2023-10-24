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
from datetime import datetime # On peut ajouter l'heure de l'envoi du message


# !!! Work with CANVAS
class Interface:
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, TITLE):
        """"
        Creates the main application window
        """
        # Initialize variables
        self.messages = []
        self.input_text = None
        self.background_label = None
        self.background_image = None
        self.background_photo = None
        self.colorMe = "lightgreen"
        self.colorOther = "lightblue"
        self.text_color = "black"

        # Set window width and height
        self.screen_width = WINDOW_WIDTH
        self.screen_height = WINDOW_HEIGHT

        # Set input box height
        self.input_box_height = 40

        self.button_size = self.input_box_height

        # Set window title
        self.title = TITLE

        # self.style = ttk.Style()
        # self.style.configure("Message.TFrame", background="lightblue")
        # self.style.configure("Sender.TLabel", background="lightblue", foreground="black")

        # Create the main application window
        self.root = Tk()

        # Set window size and Open the window in the center of the screen
        self.root.geometry(
            f"{self.screen_width}x{self.screen_height}+{int(self.root.winfo_screenwidth() / 2 - self.screen_width / 2)}+{0}")  # !!! + THAN 80 CHR.
        # Set window title and icon
        self.root.title(self.title)
        self.root.iconbitmap("icon.ico")

        self.background_image = tk.PhotoImage(file="background.png")

        # Background to be added to message frame not canvas
        self.messages_frame = ttk.Frame(self.root, style="Message.TFrame", height=300)
        self.messages_frame.pack(fill=tk.BOTH, expand=True)

        # Add a label to the frame to display the background image
        background_label = ttk.Label(self.messages_frame, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        # Create a canvas to hold the chat window
        self.canvas = tk.Canvas(self.messages_frame, width=self.screen_width,
                                height=(self.screen_height - self.input_box_height))

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

        self.canvas.bind('<Configure>', self.canvas.config(scrollregion=self.canvas.bbox("all")))

        # Add the input box
        shift = self.input_box_height
        print(shift)
        self.input_box = tk.Entry(self.root, width=WINDOW_WIDTH // 10 - shift // 8, bg="white", fg="black",
                                  font=("Comic Sans MS", 12), borderwidth=2, relief="sunken")

        # self.input_box.place(x=0, y=self.root.winfo_height() - self.input_box_height,
        #                      height=self.input_box_height, width=self.root.winfo_width() - self.button_size)
        self.input_box.pack(side=tk.LEFT)
        # Add the send button and display it
        send_icon = ImageTk.PhotoImage(
            Image.open("send_icon.png").resize((int(self.button_size * 0.8), int(self.button_size * 1)),
                                               Image.BOX))  # I didn't put self

        self.send_button = tk.Button(self.root, height=int(self.button_size * 0.8), width=int(self.button_size * 1),
                                     text='Click Me !',
                                     image=send_icon, command=lambda: self.ajouter_message())

        self.send_button.pack(side=tk.LEFT)
        # self.send_button.place(x=(self.screen_width-self.button_size), y=(self.screen_height-self.button_size))

        self.messages = []

        self.root.resizable(width=False, height=False)

        self.checkNewMessage()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.mainloop()

    def on_close(self):
        localClient.send(localClient.DISCONNECT_MESSAGE)
        self.root.destroy()
        quit()

    def scroll(self):
        self.canvas.yview_moveto(1)

    def checkNewMessage(self):
        # Check if the chat file was found and loaded
        if localClient.loadChatFile and localClient.newMessage:
            self.display_messageList()
            localClient.loadChatFile = False
            localClient.newMessage = False

        # Check if there are new messages
        if localClient.newMessage:
            # Display the messages
            self.display_message(localClient.message_list[-1])
            localClient.newMessage = False

        # Check again in 100ms
        self.root.after(100, self.checkNewMessage)

    # Take the input and move everything up
    def ajouter_message(self):
        """
        Sends the input text to the server and doesn't display it.
        Doesn't send the input text if it's empty.
        """
        self.input_text = self.input_box.get()  # Get input
        if self.input_text == "" or self.input_text == " ":
            return
        localClient.send(self.input_text)
        if self.input_text == localClient.DISCONNECT_MESSAGE:
            self.on_close()
        self.messages.append(self.input_text)
        self.create_message_frame(self.input_text, localClient.login, self.canvas_frame)
        self.create_message_frame(self.input_text, "Other", self.canvas_frame)
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.scroll()
        self.input_box.delete("0", tk.END)  # Clear input from beginning to end

    def create_message_frame(self, message, who, where):
        frame = ttk.Frame(where)
        now = datetime.now().strftime("%H:%M:%S")
        sender = ttk.Label(frame, text=f"{who}, sent at:{now}", font=("Comic Sans MS", 8, "italic"))
        sender.grid(column=0, row=0, sticky="w")
        if who==localClient.login:
            ###!!! Y A ENCORE A REFORMATER LE HEIGHT POUR ADAPTER A LA TAILLE DU TEXTE
            message_text = tk.Text(frame, wrap=tk.WORD, width=self.screen_width, height=1, bg=self.colorMe)
        else:
            message_text = tk.Text(frame, wrap=tk.WORD, width=self.screen_width, height=1, bg=self.colorOther)
        message_text.insert(tk.END, f"{message}")
        message_text.config(state=tk.DISABLED)  # A comprendre?
        message_text.grid(column=0, row=1, sticky="w")
        frame.grid(column=0, row=where.grid_size()[1], sticky="w")
        where.grid_columnconfigure(0, weight=1)

    def display_message(self, message):
        pass
    #     # for i, (message, who) in enumerate(self.messages):
    #     # Get the messages from the server
    #     # self.messages = localClient.message_list
    #     who, msg = message
    #
    #     # Check if the message is from the local client
    #     if who == localClient.login:
    #         # put box in which there will be text message label
    #         message_frame = tk.Frame(self.canvas, bg=self.colorMe) #, relief=tk.GROOVE)
    #         message_frame.pack(padx=5, pady=5, anchor=tk.NW)
    #
    #         message_label = tk.Label(message_frame, text=f"{who}: {msg}", wraplength=self.screen_width//2, justify=tk.LEFT,
    #                                  bg=self.colorMe, fg=self.text_color)
    #     # If the message is from another client
    #     else:
    #         message_frame = tk.Frame(self.canvas, bg=self.colorOther)  # , relief=tk.GROOVE)
    #         message_frame.pack(padx=5, pady=5, anchor=tk.NW)
    #
    #         message_label = tk.Label(message_frame, text=f"{who}: {msg}", wraplength=self.screen_width // 2,
    #                                  justify=tk.LEFT,
    #                                  bg=self.colorOther, fg=self.text_color)
    #     message_label.pack(padx=5, pady=5)

    def display_messageList(self):
        pass
    #     # Get the messages from the server
    #     messages = localClient.message_list
    #     # Display the messages
    #     for message in messages:
    #         self.display_message(message)


if __name__ == '__main__':
    # Create a client
    localClient = client.Client()
    # Connect the client to the server
    localClient.connect()
    try:
        print("init")
        interface = Interface(480, 700, f"Whatsdown! Logged in as: {localClient.login}")
    except Exception as e:
        print(f"[EXCEPTION] {e} occurred")
        sys.exit()
