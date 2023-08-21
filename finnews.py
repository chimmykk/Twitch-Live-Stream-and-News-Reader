import os
import subprocess
import time
import pyautogui
import json
import requests

# Global variables for the application process
app_process = None
app_opened = False
application_path = r'C:\Users\paperspace\Downloads\AllCharactersAI_v0.18\AllCharactersAI_v0.18\Windows\Chatbot_Characters.exe'

def fetch_news(category):
    """Fetches news from the News API based on the provided category."""
    url = f"https://newsapi.org/v2/everything?q={category}&language=en&sortBy=publishedAt&apiKey=0d82bbd91c974f81ae2df4b190404fbd"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        articles = data["articles"]
        
        # Create a list of dictionaries containing truncated description and source
        news_items = [{"title": article["title"], "description": truncate_description(article["description"], 25), "source": article["source"]["name"], "publishedAt": article["publishedAt"]} for article in articles]
        
        return news_items[:3]  # Return only the first 3 news items for each category
    else:
        return None

def truncate_description(description, num_words):
    """Truncate the description to end in 'num_words' words."""
    words = description.split()
    if len(words) > num_words:
        truncated_words = " ".join(words[:num_words])
        return truncated_words + "..."
    return description

def main():
    global app_process, app_opened

    categories = ["crypto", "sports", "weather", "worldnews"]
    num_articles_to_save = 10

    # Open the application if it is not already open
    if not app_opened:
        app_process = subprocess.Popen([application_path])
        app_opened = True
        # Wait for the application to open (adjust the sleep time as needed)
        time.sleep(2)
        # Press "Tab" key three times to navigate to the Doge option
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        # Press "Enter" key to select the Doge option
        pyautogui.press('enter')

    try:
        for category in categories:
            news_items = fetch_news(category)
            if news_items is not None:
                news_counter = 0
                for news_item in news_items:
                    print("Category:", category.capitalize())
                    print("Title:", news_item["title"])
                    print("Description:", news_item["description"])
                    print("Source:", news_item["source"])
                    print("Published At:", news_item["publishedAt"])
                    print()  # Add an empty line between each news item
                    
                    automate_chatbot_with_message(news_item["description"])
                    time.sleep(50)  # Wait for 10 seconds before processing the next message
                    news_counter += 1
                    if news_counter >= 3:
                        break  # Switch to the next category after fetching 2 news for the current category
            else:
                print(f"Failed to fetch {category} news.")
    except KeyboardInterrupt:
        close_application()

def automate_chatbot_with_message(truncated_description):
    global app_process, app_opened

    # Perform the automation steps using the opened application
    if app_opened:
        # Trigger three tabs
        pyautogui.rightClick()
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')

        # Type the 'say' message into the application           say "Blockchain sec"
        pyautogui.typewrite(f'Repeat after me "{truncated_description}"')

        # Press "Enter" key to send the message
        pyautogui.press('enter')

def close_application():
    global app_process, app_opened
    if app_process and app_process.poll() is None:
        app_process.terminate()
        app_process.wait()
    app_opened = False

if __name__ == '__main__':
    main()