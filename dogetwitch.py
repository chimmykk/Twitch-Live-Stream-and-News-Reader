import os
import socket
import subprocess
import time
import pyautogui

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
    # Clear console before connecting to the IRC server
    os.system('cls' if os.name == 'nt' else 'clear')

    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\r\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
    sock.send(f"JOIN #{channel}\r\n".encode('utf-8'))

    try:
        while True:
            resp = sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                message = resp.split(':')[-1].strip()

                # Clear console before printing the new message
                os.system('cls' if os.name == 'nt' else 'clear')

                if not message.startswith('End of /NAMES list'):
                    print(message)

                    # Store the message to a text file
                    store_message_to_file(message)

                    # Automate chatbot using the message from the console
                    automate_chatbot_with_message(message)

    except KeyboardInterrupt:
        sock.close()
        exit()


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