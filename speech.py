import speech_recognition as sr
import tkinter as tk
from tkinter import messagebox

class SpeechRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Speech Recognition App")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f2f5")
        
        # Initialize recognizer
        self.recognizer = sr.Recognizer()
        
        # GUI components
        self.label = tk.Label(root, text="Press 'Start' to begin speaking", bg="#f0f2f5", font=("Arial", 14))
        self.label.pack(pady=20)
        
        self.output_text = tk.Text(root, wrap="word", font=("Arial", 12), width=50, height=10, bg="#ffffff", state="disabled")
        self.output_text.pack(pady=10)
        
        self.start_button = tk.Button(root, text="Start Listening", command=self.start_listening, bg="#4caf50", fg="white", font=("Arial", 12), width=15)
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="Stop Listening", command=self.stop_listening, bg="#f44336", fg="white", font=("Arial", 12), width=15, state="disabled")
        self.stop_button.pack(pady=5)

        self.is_listening = False

    def start_listening(self):
        self.is_listening = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.label.config(text="Listening... Speak now.")

        # Start listening in a separate thread
        self.root.after(100, self.recognize_speech)

    def stop_listening(self):
        self.is_listening = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.label.config(text="Press 'Start' to begin speaking again")

    def recognize_speech(self):
        if not self.is_listening:
            return
        
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                # Capture audio from the microphone
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                # Recognize speech using Google Web Speech API
                text = self.recognizer.recognize_google(audio)
                self.update_output_text(f"You said: {text}\n")
            except sr.UnknownValueError:
                self.update_output_text("Could not understand audio.\n")
            except sr.RequestError as e:
                self.update_output_text(f"Could not request results; {e}\n")
            except Exception as e:
                self.update_output_text(f"An error occurred: {e}\n")

        # Keep listening if the flag is set
        if self.is_listening:
            self.root.after(100, self.recognize_speech)

    def update_output_text(self, text):
        self.output_text.config(state="normal")
        self.output_text.insert(tk.END, text)
        self.output_text.config(state="disabled")
        self.output_text.yview(tk.END)  

# Create and run the application
root = tk.Tk()
app = SpeechRecognitionApp(root)
root.mainloop()
