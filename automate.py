import os
import socket
import subprocess
import time
import pyautogui

server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'rilsos'
token = 'oauth:wb7ph6zjttttvdtk9x3uz27vy8umdi'
channel = 'dylansafeass'

output_folder = "tobereadnow"
file_counter = 1

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
    # Press "Tab" key three times to navigate to the Doge option
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')

    # Press "Enter" key to select the Doge option
    pyautogui.press('enter')

    time.sleep(2)

    # Press "Tab" key three times to trigger three tabs again
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')

    time.sleep(2)

    # Type the message from the console
    pyautogui.typewrite(message)

    # Press "Enter" key to send the message
    pyautogui.press('enter')


if __name__ == '__main__':
    main()