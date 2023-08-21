import os
import socket
import subprocess
import time
import pyautogui
import tkinter as tk
from tkinter import scrolledtext, Button, StringVar, Radiobutton
import requests
import json

# Global variables for Twitch Chatbot
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

def fetch_news(category):
    """Fetches news from the News API based on the provided category."""
    url = f"https://newsapi.org/v2/everything?q={category}&language=en&sortBy=publishedAt&apiKey=0d82bbd91c974f81ae2df4b190404fbd"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        return data["articles"]
    else:
        return None

def truncate_description(description, num_words):
    """Truncate the description to end in 'num_words' words."""
    words = description.split()
    if len(words) > num_words:
        truncated_words = " ".join(words[:num_words])
        return truncated_words + "..."
    return description

def automate_chatbot(message):
    subprocess.Popen([application_path])

    time.sleep(2)

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

    # Type the provided message
    pyautogui.typewrite(message)

    # Press "Enter" key to send the message
    pyautogui.press('enter')

def twitch_chatbot():
    # Clear console before connecting to the IRC server
    os.system('cls' if os.name == 'nt' else 'clear')

    sock = socket.socket()
    sock.connect((server, port))
    sock.send(f"PASS {token}\r\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
    sock.send(f"JOIN #{channel}\r\n".encode('utf-8'))

    try:
        while True:
            # Update the UI to keep it responsive
            root.update()

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

def on_start_button_click():
    choice = option_var.get()
    if choice == "twitch":
        # Start the Twitch Chatbot
        twitch_chatbot()
    elif choice == "news":
        # Start the news fetching and chatbot automation
        start_news()

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

def start_news():
    categories = ["crypto", "sports", "weather", "worldnews"]
    num_articles_to_save = 10

    for category in categories:
        news = fetch_news(category)
        if news is not None:
            for article in news[:num_articles_to_save]:
                title = article["title"]
                description = article["description"]
                truncated_description = truncate_description(description, 25)

                print(f"Category: {category.capitalize()}")
                print("Title:", title)
                print(f'Say "{truncated_description}"')
                print()

                time.sleep(50)  # Pause for 10 seconds before displaying the next article

                # Pass the dynamically generated message to the automate_chatbot() function
                automate_chatbot(f'Say "{truncated_description}"')
        else:
            print(f"Failed to fetch {category} news.")

def create_gui():
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

    # Option variable to track the user's choice
    option_var = StringVar()
    option_var.set("")  # Initialize as an empty string

    # Radio buttons for the user to choose between Twitch and News
    twitch_radio = Radiobutton(root, text="Twitch Chatbot", variable=option_var, value="twitch")
    twitch_radio.grid(row=1, column=2, padx=5)

    news_radio = Radiobutton(root, text="Start News", variable=option_var, value="news")
    news_radio.grid(row=1, column=3, padx=5)

    # Create a label for the ticker display
    ticker_label = tk.Label(root, text="", wraplength=500, font=("Arial", 12), anchor="w")
    ticker_label.grid(row=2, column=0, columnspan=3, pady=10)

    # Create the "Start" button
    start_button = Button(root, text="Start", command=on_start_button_click)
    start_button.grid(row=1, column=4, padx=5)

    return root, output_area, ticker_label, option_var

if __name__ == '__main__':
    # Create the GUI
    root, output_area, ticker_label, option_var = create_gui()

    # Start the Tkinter main loop to keep the GUI responsive
    root.mainloop()
