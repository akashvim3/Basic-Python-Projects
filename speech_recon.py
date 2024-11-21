import time
import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import pyttsx3


class SpeechRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Speech Recognition App")
        self.root.geometry("600x600")
        self.root.configure(bg="#f0f2f5")

        # Initialize recognizer
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.is_listening = False
        self.auto_scroll = tk.BooleanVar(value=True)
        self.is_paused = False

        # GUI Components
        self.setup_ui()

    def setup_ui(self):
        """Set up the GUI components."""
        title_font = ("Arial", 16, "bold")
        label_font = ("Arial", 14)
        button_font = ("Arial", 12)

        # Title
        tk.Label(self.root, text="Speech Recognition App", font=title_font, bg="#f0f2f5").pack(pady=10)

        # Output Text Area
        self.output_text = tk.Text(
            self.root, wrap="word", font=("Arial", 12), width=60, height=15, bg="#ffffff", state="disabled"
        )
        self.output_text.pack(pady=10)

        # Auto-scroll toggle
        tk.Checkbutton(
            self.root, text="Enable Auto-Scroll", variable=self.auto_scroll, font=("Arial", 10), bg="#f0f2f5"
        ).pack(pady=5)

        # Buttons
        button_frame = tk.Frame(self.root, bg="#f0f2f5")
        button_frame.pack(pady=10)

        self.start_button = tk.Button(
            button_frame,
            text="Start Listening",
            command=self.start_listening,
            bg="#4caf50",
            fg="white",
            font=button_font,
            width=15,
        )
        self.start_button.grid(row=0, column=0, padx=5)

        self.pause_button = tk.Button(
            button_frame,
            text="Pause Listening",
            command=self.pause_listening,
            bg="#f0ad4e",
            fg="white",
            font=button_font,
            width=15,
            state="disabled",
        )
        self.pause_button.grid(row=0, column=1, padx=5)

        self.stop_button = tk.Button(
            button_frame,
            text="Stop Listening",
            command=self.stop_listening,
            bg="#f44336",
            fg="white",
            font=button_font,
            width=15,
            state="disabled",
        )
        self.stop_button.grid(row=1, column=0, padx=5, pady=5)

        self.clear_button = tk.Button(
            button_frame,
            text="Clear Text",
            command=self.clear_text,
            bg="#607d8b",
            fg="white",
            font=button_font,
            width=15,
        )
        self.clear_button.grid(row=1, column=1, padx=5, pady=5)

        self.save_button = tk.Button(
            self.root,
            text="Save to File",
            command=self.save_to_file,
            bg="#5bc0de",
            fg="white",
            font=button_font,
            width=15,
        )
        self.save_button.pack(pady=5)

        self.play_button = tk.Button(
            self.root,
            text="Play Text as Audio",
            command=self.play_text,
            bg="#795548",
            fg="white",
            font=button_font,
            width=15,
        )
        self.play_button.pack(pady=5)

        # Listening Indicator
        self.listening_indicator = tk.Label(self.root, text="", bg="#f0f2f5", font=("Arial", 10), fg="red")
        self.listening_indicator.pack(pady=10)

        # Theme Switcher
        tk.Button(
            self.root,
            text="Toggle Dark Mode",
            command=self.toggle_theme,
            bg="#9c27b0",
            fg="white",
            font=button_font,
            width=15,
        ).pack(pady=10)

    def start_listening(self):
        """Start listening for speech."""
        self.is_listening = True
        self.is_paused = False
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.pause_button.config(state="normal")
        self.listening_indicator.config(text="Listening... Speak now.")

        # Start speech recognition in a separate thread
        threading.Thread(target=self.recognize_speech).start()

    def pause_listening(self):
        """Pause speech recognition."""
        self.is_paused = not self.is_paused
        state_text = "Resuming..." if self.is_paused else "Paused."
        self.listening_indicator.config(text=state_text)
        self.pause_button.config(text="Resume Listening" if self.is_paused else "Pause Listening")

    def stop_listening(self):
        """Stop listening for speech."""
        self.is_listening = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.pause_button.config(state="disabled", text="Pause Listening")
        self.listening_indicator.config(text="")

    def recognize_speech(self):
        """Recognize speech and display it in the text area."""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                while self.is_listening:
                    if self.is_paused:
                        time.sleep(0.5)
                        continue
                    self.listening_indicator.config(text="Listening... Speak now.")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    try:
                        text = self.recognizer.recognize_google(audio)
                        self.update_output_text(f"You said: {text}\n")
                    except sr.UnknownValueError:
                        self.update_output_text("Could not understand audio.\n")
                    except sr.RequestError as e:
                        self.update_output_text(f"Request error: {e}\n")
        except Exception as e:
            self.update_output_text(f"Error: {e}\n")

    def update_output_text(self, text):
        """Update the output text area."""
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, text)
        self.output_text.config(state="disabled")
        if self.auto_scroll.get():
            self.output_text.yview(tk.END)

    def clear_text(self):
        """Clear the text area."""
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state="disabled")

    def save_to_file(self):
        """Save the recognized text to a file."""
        text = self.output_text.get(1.0, tk.END).strip()
        if text:
            with open("recognized_speech.txt", "w") as file:
                file.write(text)
            messagebox.showinfo("Success", "Text saved to recognized_speech.txt")
        else:
            messagebox.showwarning("Warning", "No text to save.")

    def play_text(self):
        """Play the recognized text as audio."""
        text = self.output_text.get(1.0, tk.END).strip()
        if text:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            messagebox.showwarning("Warning", "No text to play.")

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        current_bg = self.root.cget("bg")
        if current_bg == "#f0f2f5":
            self.root.configure(bg="#2b2b2b")
            self.output_text.configure(bg="#333333", fg="#ffffff")
            self.listening_indicator.configure(bg="#2b2b2b", fg="#f0f2f5")
        else:
            self.root.configure(bg="#f0f2f5")
            self.output_text.configure(bg="#ffffff", fg="#000000")
            self.listening_indicator.configure(bg="#f0f2f5", fg="red")


# Create and run the application
root = tk.Tk()
app = SpeechRecognitionApp(root)
root.mainloop()
