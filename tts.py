import os
import subprocess
import time
import pyautogui

# Global variables
input_folder = "todynews"
file_counter = 1

# Variables for the application process
app_process = None
app_opened = False
application_path = r'C:\Users\paperspace\Downloads\AllCharactersAI_v0.18\AllCharactersAI_v0.18\Windows\Chatbot_Characters.exe'

def main():
    global file_counter  # Make file_counter global

    # Clear console before starting
    os.system('cls' if os.name == 'nt' else 'clear')

    while True:
        filename = f"{input_folder}/{file_counter}.txt"
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                message = file.read()

            # Clear console before printing the new message
            os.system('cls' if os.name == 'nt' else 'clear')
            print(message)

            # Automate chatbot using the message from the file
            automate_chatbot_with_message(message)

            # Increment the file counter
            file_counter += 1

        # Wait for 3 minutes before processing the next file
        time.sleep(180)


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