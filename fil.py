import os
import socket
import subprocess
import time
import pyautogui
import tkinter as tk
from tkinter import scrolledtext, Button

# Global variables
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'rilsos'
token = 'oauth:sp86qcmj6kvbqfz6pqmt8nbsvk5sj4'
channel = 'thedogeai'

output_folder = "tobereadnow"
file_counter = 1

# Variables for the application process
app_process = None
app_opened = False
application_path = r'C:\Users\paperspace\Downloads\AllCharactersAI_v0.18\AllCharactersAI_v0.18\Windows\Chatbot_Characters.exe'

def main():
    # Create the UI
    root = tk.Tk()
    root.title("Twitch Chatbot")

    output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
    output_area.grid(row=0, column=0, columnspan=3)

    def clear_output():
        output_area.delete("1.0", tk.END)

    clear_button = Button(root, text="Clear Output", command=clear_output)
    clear_button.grid(row=1, column=0)

    stop_button = Button(root, text="Stop Bot", command=root.quit)
    stop_button.grid(row=1, column=1)

    # Create a label for the ticker display
    ticker_label = tk.Label(root, text="", wraplength=500, font=("Arial", 12), anchor="w")
    ticker_label.grid(row=2, column=0, columnspan=3, pady=10)

    # Clear console before connecting to the IRC server
    os.system('cls' if os.name == 'nt' else 'clear')

    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\r\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
    sock.send(f"JOIN #{channel}\r\n".encode('utf-8'))

    try:
        while True:
            root.update()  # Update the UI to keep it responsive

            resp = sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                message = resp.split(':')[-1].strip()

                # Clear console before printing the new message
                output_area.delete("1.0", tk.END)
                if not message.startswith('End of /NAMES list'):
                    output_area.insert(tk.END, message)

                # Store the message to a text file
                store_message_to_file(message)

                # Update the ticker with the latest message
                ticker_label.config(text=message)

                # Automate chatbot using the message from the console
                automate_chatbot_with_message(message)

    except KeyboardInterrupt:
        sock.close()
        root.destroy()

def store_message_to_file(message):
    global file_counter
    filename = f"{output_folder}/{file_counter}.txt"
    with open(filename, 'w') as file:
        file.write(message)
    file_counter += 1

def automate_chatbot_with_message(message):
    global app_process, app_opened

    if not app_opened:
        # Open the application if it is not already open
        app_process = subprocess.Popen([application_path])
        app_opened = True

        # Wait for the application to open (adjust the sleep time as needed)
        time.sleep(5)

    # Perform the automation steps using the opened application
    if app_opened:
        # Trigger three tabs
        pyautogui.rightClick()
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
     
        # Type the latest message received
        pyautogui.typewrite(message)

        # Press "Enter" key to send the message
        pyautogui.press('enter')

if __name__ == '__main__':
    main()