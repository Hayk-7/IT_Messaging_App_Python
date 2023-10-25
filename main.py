# encode: utf-8
"""
Created on 4/10/23 13:00

@author: H, R
"""

import client
import interface

if __name__ == '__main__':
    # Create a client
    localClient = client.Client()
    # Connect the client to the server
    localClient.connect()
    try:
        print("init")
        interface = interface.Interface(480, 700, f"Whatsdown! Logged in as: {localClient.login}", localClient)
    except Exception as e:
        print(f"[EXCEPTION] {e} occurred")
        quit()
