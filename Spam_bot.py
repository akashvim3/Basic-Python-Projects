import pyautogui
import time
import datetime
import random
import tkinter as tk
from tkinter import ttk, messagebox
from plyer import notification
import json
import os
from playsound import playsound
import threading

# Constants
SOUND_FILE = "alert.mp3"  # Replace with the path to your sound file
REMINDERS_FILE = "reminders.json"

# Function to save reminders to a file
def save_reminders(reminders):
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f)

# Function to load reminders from a file
def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, 'r') as f:
            return json.load(f)
    return []

# Function to show a desktop notification
def show_notification(message):
    notification.notify(
        title="Reminder",
        message=message,
        timeout=10  # Seconds
    )

# Function to play a sound alert
def play_sound():
    try:
        playsound(SOUND_FILE)
    except Exception as e:
        print(f"Error playing sound: {e}")

# Reminder loop function (runs in the background)
def reminder_loop(reminders):
    while True:
        for reminder in reminders:
            print(f"[{datetime.datetime.now()}] Reminder: {reminder['reminder']}")

            # Show desktop notification
            show_notification(reminder['reminder'])

            # Play sound alert
            play_sound()

            # Type the reminder in active application
            pyautogui.typewrite(f"Reminder: {reminder['reminder']}")
            pyautogui.press("enter")

            # Wait for the next interval
            time.sleep(reminder['interval'] + random.randint(1, 10))  

# Function to update the GUI list of reminders
def update_reminder_list(reminder_listbox, reminders):
    reminder_listbox.delete(0, tk.END)
    for reminder in reminders:
        reminder_listbox.insert(tk.END, f"{reminder['reminder']} (Every {reminder['interval']} sec)")

# Function to add a new reminder
def add_reminder(reminders, reminder_text, interval, reminder_listbox):
    reminders.append({'reminder': reminder_text, 'interval': interval})
    save_reminders(reminders)
    update_reminder_list(reminder_listbox, reminders)

# Function to edit an existing reminder
def edit_reminder(reminders, selected_index, new_reminder_text, new_interval, reminder_listbox):
    if selected_index is not None and 0 <= selected_index < len(reminders):
        reminders[selected_index] = {'reminder': new_reminder_text, 'interval': new_interval}
        save_reminders(reminders)
        update_reminder_list(reminder_listbox, reminders)

# Function to delete a selected reminder
def delete_reminder(reminders, selected_index, reminder_listbox):
    if selected_index is not None and 0 <= selected_index < len(reminders):
        reminders.pop(selected_index)
        save_reminders(reminders)
        update_reminder_list(reminder_listbox, reminders)

# Main GUI function
def open_gui(reminders):
    # Create the main window
    window = tk.Tk()
    window.title("Reminder Application")
    window.geometry("500x400")
    window.configure(bg="#f0f0f0")

    # Fonts and styles
    title_font = ("Helvetica", 16, "bold")
    label_font = ("Arial", 12)
    button_font = ("Arial", 10)

    # Title
    tk.Label(window, text="Reminder Manager", font=title_font, bg="#f0f0f0").pack(pady=10)

    # Reminder list
    reminder_listbox = tk.Listbox(window, font=label_font, width=50, height=10)
    reminder_listbox.pack(pady=10)
    update_reminder_list(reminder_listbox, reminders)

    # Add reminder frame
    add_frame = tk.Frame(window, bg="#f0f0f0")
    add_frame.pack(pady=10)

    tk.Label(add_frame, text="Reminder:", font=label_font, bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
    reminder_entry = tk.Entry(add_frame, font=label_font, width=30)
    reminder_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(add_frame, text="Interval (sec):", font=label_font, bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
    interval_entry = tk.Entry(add_frame, font=label_font, width=10)
    interval_entry.grid(row=1, column=1, padx=5, pady=5)

    def on_add_reminder():
        reminder_text = reminder_entry.get()
        interval = int(interval_entry.get())
        if reminder_text and interval > 0:
            add_reminder(reminders, reminder_text, interval, reminder_listbox)
            reminder_entry.delete(0, tk.END)
            interval_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Invalid Input", "Please enter valid reminder text and interval.")

    tk.Button(add_frame, text="Add Reminder", font=button_font, command=on_add_reminder).grid(row=2, column=0, columnspan=2, pady=10)

    # Edit and Delete buttons
    def on_edit_reminder():
        selected_index = reminder_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            new_reminder_text = reminder_entry.get()
            new_interval = int(interval_entry.get())
            if new_reminder_text and new_interval > 0:
                edit_reminder(reminders, selected_index, new_reminder_text, new_interval, reminder_listbox)
            else:
                messagebox.showwarning("Invalid Input", "Please enter valid reminder text and interval.")
        else:
            messagebox.showwarning("No Selection", "Please select a reminder to edit.")

    def on_delete_reminder():
        selected_index = reminder_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            delete_reminder(reminders, selected_index, reminder_listbox)
        else:
            messagebox.showwarning("No Selection", "Please select a reminder to delete.")

    tk.Button(window, text="Edit Reminder", font=button_font, command=on_edit_reminder).pack(pady=5)
    tk.Button(window, text="Delete Reminder", font=button_font, command=on_delete_reminder).pack(pady=5)

    # Run the main loop
    window.mainloop()

# Main function
if __name__ == "__main__":
    # Load saved reminders if any
    reminders = load_reminders()

    # Start the reminder loop in a separate thread
    threading.Thread(target=reminder_loop, args=(reminders,), daemon=True).start()

    # Open the GUI
    open_gui(reminders)
