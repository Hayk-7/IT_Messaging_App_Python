# encode: utf-8
"""
Created on 4/10/23 13:00

@author: H, R
"""

import client
import interface

if __name__ == '__main__':
    try:
        # Create the login page
        # login_page = interface.WhatsDownLoginPage(480, 700)
        # login = ""
        # while login == "" or login.isspace():
        #     login = login_page.login
        login = input("Enter your login: ")

        # Create a client
        localClient = client.Client(login)
        # Connect the client to the server
        localClient.connect()

        # Create the main window
        interface = interface.WhatsDownMainWindow(480, 700, localClient)

    except Exception as e:
        print(f"[EXCEPTION] {e} occurred")
        quit()
