import os
import subprocess
import time
import pyautogui
import json
import requests
import threading
import pyperclip

# Global variables for the application process
app_process = None
app_opened = False
application_path = r'C:\Users\paperspace\Downloads\AllCharactersAI_v0.26_Doge_GS\AllCharactersAI_v0.26_Doge_GS\Windows\Chatbot_Characters.exe'  # New application path

def fetch_news(category):
    url = f"https://newsapi.org/v2/everything?q={category}&language=en&sortBy=publishedAt&apiKey=0d82bbd91c974f81ae2df4b190404fbd"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        articles = data["articles"]
        news_items = [{"title": article["title"], "description": truncate_description(article["description"], 25), "source": article["source"]["name"], "publishedAt": article["publishedAt"]} for article in articles]
        return news_items[:3]
    else:
        return None

def truncate_description(description, num_words):
    words = description.split()
    if len(words) > num_words:
        truncated_words = " ".join(words[:num_words])
        return truncated_words + "..."
    return description

def main():
    global app_process, app_opened

    categories = ["crypto", "sports", "weather", "worldnews"]
    num_articles_to_save = 10

    if not app_opened:
        app_process = subprocess.Popen([application_path])
        app_opened = True
        time.sleep(2)
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('enter')

    try:
        delete_thread = threading.Thread(target=auto_delete_file, args=('readthis/read.txt', 20))
        delete_thread.start()

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
                    print()

                    automate_chatbot_with_message(news_item)

                    save_path = os.path.join('readthis', 'read.txt')
                    with open(save_path, 'a') as file:
                        # Save to read.txt without the "Repeat after this:" prefix
                        file.write(f'{news_item["title"]}  {news_item["description"]} The source of this information is from {news_item["source"]}\n')

                    time.sleep(15)
                    news_counter += 1
                    if news_counter >= 3:
                        break

            else:
                print(f"Failed to fetch {category} news.")
    except KeyboardInterrupt:
        close_application()

def automate_chatbot_with_message(news_item):
    pyautogui.leftClick()
    pyautogui.press('tab')
    pyautogui.press('tab')
    pyautogui.press('tab')

    formatted_message = f'Repeat after this: {news_item["title"]}\n  {news_item["description"]} The source of this information is from {news_item["source"]}'
    pyperclip.copy(formatted_message)

    # Simulate paste action using Ctrl+V
    pyautogui.hotkey('ctrl', 'v')

    pyautogui.press('enter')

def close_application():
    global app_process, app_opened
    if app_process and app_process.poll() is None:
        app_process.terminate()
        app_process.wait()
    app_opened = False

def auto_delete_file(file_path, interval):
    while True:
        time.sleep(interval)
        with open(file_path, 'w') as file:
            pass

if __name__ == '__main__':
    main()