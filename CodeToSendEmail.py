import requests
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os
import json

# CONFIGURATION
FINNHUB_API_KEY = 'd0obvjpr01qsib2bmb70d0obvjpr01qsib2bmb7g'  # Replace with your real key
STOCK_SYMBOL = 'RIVN'

EMAIL_FROM = 'micdiw@yahoo.com'
EMAIL_TO = 'michel.diwan@gmail.com'
EMAIL_PASSWORD = 'umslgdixngqoqcfd'  # Use an app password if using Gmail
SMTP_SERVER = 'smtp.mail.yahoo.com'
SMTP_PORT = 587

STATE_FILE = 'last_price.json'

# === FUNCTIONS ===

def get_rivn_price():
    url = f'https://finnhub.io/api/v1/quote?symbol={STOCK_SYMBOL}&token={FINNHUB_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data['c']  # current price

ef load_last_price():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            data = json.load(f)
            return data.get('price')
    return None

def save_current_price(price):
    with open(STATE_FILE, 'w') as f:
        json.dump({'price': price}, f)

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        current_price = get_rivn_price()
        last_price = load_last_price()

        if last_price:
            percent_change = ((current_price - last_price) / last_price) * 100
            change_str = f"{percent_change:+.2f}%"
        else:
            change_str = "AWS - N/A (no prior price recorded)"

        save_current_price(current_price)

        message = (
            f"[{now}]\n"
            f"AWS - RIVN current price: ${current_price:.2f}\n"
            f"AWS - Change since last recorded: {change_str}"
        )

        print(message)
        send_email(f"RIVN Price Update - {now}", message)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
