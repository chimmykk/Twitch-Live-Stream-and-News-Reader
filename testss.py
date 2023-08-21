import subprocess
import time
import pyautogui
import os
import dropbox
from dropbox.exceptions import AuthError

# Dropbox access token
DROPBOX_ACCESS_TOKEN = 'sl.BiPzj-ovGf1Zx-WMSN56Md1e_Ffp5VEK7xUh7tnI1KB90owFDTPGnMZhyeHMDFTs9EQnURlyyzVF4x1dfuOkkmpLjJP2nbneEEggYtGOowPaV3fbFp4mAZ26wVvjPqDDGDO3IN5npF0'

# Folder path to check for videos
VIDEO_FOLDER_PATH = r'C:\Users\paperspace\Videos\Chatbot_characters'

def upload_video_to_dropbox(video_path):
    # Initialize Dropbox client
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

    try:
        # Upload the video file to Dropbox
        with open(video_path, 'rb') as file:
            dbx.files_upload(file.read(), '/' + os.path.basename(video_path))
        print("Video uploaded to Dropbox successfully.")
    except AuthError as e:
        print("Error authenticating with Dropbox.")
    except dropbox.exceptions.ApiError as e:
        print("Error uploading video to Dropbox:", e)

def automate_chatbot_and_upload():
    # Open the chatbot application
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

    # Type "what is your name"
    pyautogui.typewrite("DO YOU KNOW NARENRA MODI")

    # Press "Enter" key to send the message
    pyautogui.press('enter')

    # Add a 2-second delay
    time.sleep(2)

    # Enable screen recording
    pyautogui.hotkey('alt', 'f9')

    # Wait for 1 minute
    time.sleep(60)

    # Close the application
    pyautogui.hotkey('alt', 'f4')

    # Check for video files in the folder and upload to Dropbox
    video_files = [file for file in os.listdir(VIDEO_FOLDER_PATH) if file.endswith('.mp4')]
    if video_files:
        print("Found video files:", video_files)
        for video_file in video_files:
            video_path = os.path.join(VIDEO_FOLDER_PATH, video_file)
            upload_video_to_dropbox(video_path)
    else:
        print("No video files found in the folder.")

automate_chatbot_and_upload()