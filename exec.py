import subprocess
import time
import pyautogui
import os
import requests
import json

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
    subprocess.Popen(r'C:\Users\paperspace\Downloads\AllCharactersAI_v0.18\AllCharactersAI_v0.18\Windows\Chatbot_Characters.exe')

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

if __name__ == "__main__":
    categories = ["crypto", "sports", "weather", "worldnews"]
    num_articles_to_save = 2

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
            
                time.sleep(60)  # Pause for 10 seconds before displaying the next article

                # Pass the dynamically generated message to the automate_chatbot() function
                automate_chatbot(f'Say "{truncated_description}"')
        else:
            print(f"Failed to fetch {category} news.")