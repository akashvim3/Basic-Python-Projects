import schedule
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(filename="umbrella_reminder.log", level=logging.INFO)

# Email and Weather Configuration
EMAIL_ADDRESS = "jackvimal504@gmail.com"
EMAIL_PASSWORD = "your_email_password"
RECIPIENT_EMAIL = "recipient_email@gmail.com"
CITY = "Lucknow"
API_KEY = "06411e989d72de7e9582672f4e7bce53"  # Get your free API key at https://openweathermap.org/api
WEATHER_API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Function to fetch weather details
def fetch_weather():
    try:
        response = requests.get(WEATHER_API_URL)
        data = response.json()
        if data["cod"] != 200:
            raise Exception(data.get("message", "Failed to fetch weather data"))
        
        weather = {
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["description"],
        }
        return weather
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        return None

# Function to send email
def send_email(weather):
    try:
        # Email content
        subject = "Umbrella Reminder - Stay Prepared!"
        body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <h2 style="color: #2E8B57;">Good Morning!</h2>
                <p>Here's your daily weather update for <strong>{CITY}</strong>:</p>
                <ul>
                    <li><strong>Temperature:</strong> {weather['temperature']}°C</li>
                    <li><strong>Condition:</strong> {weather['condition'].capitalize()}</li>
                </ul>
                <p>
                    Based on today's weather, we recommend <strong>taking an umbrella</strong> if you're heading out.
                </p>
                <footer style="margin-top: 20px; font-size: 0.9em; color: #555;">
                    Stay safe!<br>
                    <strong>Weather Reminder Bot</strong>
                </footer>
            </body>
        </html>
        """

        # Create the email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        
        logging.info(f"Email sent successfully on {datetime.now()}")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

# Function to check weather and decide action
def check_weather_and_notify():
    weather = fetch_weather()
    if not weather:
        logging.warning("Weather data unavailable, skipping email.")
        return

    if any(word in weather["condition"].lower() for word in ["rain", "snow", "shower", "mist", "cloud"]):
        send_email(weather)

# Schedule the task
schedule.every().day.at("06:00").do(check_weather_and_notify)

# Keep the script running
if __name__ == "__main__":
    logging.info("Umbrella Reminder Bot started.")
    while True:
        schedule.run_pending()
