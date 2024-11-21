import os
import time
import threading
from tkinter import *
from telethon.sync import TelegramClient
from telethon.t1.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
from colorama import Fore, Style
import schedule
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

# Load sensitive information from environment variables
load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
token = os.getenv('BOT_TOKEN')
phone = os.getenv('YOUR_PHONE_NUMBER')
user_id = os.getenv('USER_ID')
user_hash = os.getenv('USER_HASH')

client = TelegramClient('session_name', api_id, api_hash)

# GUI setup with Tkinter
root = Tk()
root.title("Telegram Bot GUI")
root.geometry("400x400")

# Function to authenticate and connect client
def authenticate_client():
    if not client.is_user_authorized():
        print(Fore.YELLOW + "Not authorized. Sending code request...")
        client.send_code_request(phone)
        client.sign_in(phone, input(Fore.CYAN + 'Enter the code: '))
    print(Fore.GREEN + "Successfully authenticated!")

# Function to send messages
def send_message(recipient, message_text):
    try:
        if isinstance(recipient, InputPeerUser):
            client.send_message(recipient, message_text, parse_mode='html')
            print(Fore.GREEN + f"Message sent to user: {recipient.user_id}")
        elif isinstance(recipient, InputPeerChannel):
            client.send_message(recipient, message_text, parse_mode='html')
            print(Fore.GREEN + f"Message sent to channel/group: {recipient.channel_id}")
    except Exception as e:
        print(Fore.RED + f"Error sending message: {str(e)}")

# Function to schedule message
def schedule_message(message_text, time_str):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: send_message(recipient, message_text), 'date', run_date=time_str)
    scheduler.start()

# Threading function to send multiple messages concurrently
def send_message_thread(recipient, message_text):
    threading.Thread(target=send_message, args=(recipient, message_text)).start()

# Function to handle sending multiple media files
def send_media(recipient, media_paths, caption=""):
    try:
        for media_path in media_paths:
            client.send_file(recipient, media_path, caption=caption, parse_mode='html')
        print(Fore.GREEN + f"Media sent to {recipient.user_id if isinstance(recipient, InputPeerUser) else recipient.channel_id}")
    except Exception as e:
        print(Fore.RED + f"Error sending media: {str(e)}")

# Function to handle the send message button click event
def on_send_button_click():
    recipient = InputPeerUser(user_id, user_hash)  
    message_text = message_entry.get()
    send_message_thread(recipient, message_text)

# Function to handle the schedule button click event
def on_schedule_button_click():
    recipient = InputPeerUser(user_id, user_hash)  
    message_text = message_entry.get()
    time_str = time_entry.get()
    schedule_message(message_text, time_str)

# Creating the GUI elements
message_label = Label(root, text="Message:")
message_label.pack()

message_entry = Entry(root)
message_entry.pack()

send_button = Button(root, text="Send Message", command=on_send_button_click)
send_button.pack()

time_label = Label(root, text="Schedule Time (YYYY-MM-DD HH:MM:SS):")
time_label.pack()

time_entry = Entry(root)
time_entry.pack()

schedule_button = Button(root, text="Schedule Message", command=on_schedule_button_click)
schedule_button.pack()

root.mainloop()

# Main execution
if __name__ == '__main__':
    try:
        # Connect to the Telegram client
        client.connect()
        authenticate_client()

        # Send a sample message (you can replace with dynamic input)
        recipient = InputPeerUser(user_id, user_hash)  
        send_message(recipient, "This is a sample message.")

        # Optionally, send multimedia
        # media_paths = ['path_to_image_or_video1', 'path_to_image_or_video2']
        # send_media(recipient, media_paths, "Check out these media!")

        # Disconnect client after use
        client.disconnect()

    except Exception as e:
        print(Fore.RED + f"Error: {str(e)}")
