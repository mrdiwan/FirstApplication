import requests
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# CONFIGURATION
FINNHUB_API_KEY = 'd0obvjpr01qsib2bmb70d0obvjpr01qsib2bmb7g'  # Replace with your real key
STOCK_SYMBOL = 'RIVN'

EMAIL_FROM = 'micdiw@yahoo.com'
EMAIL_TO = 'michel.diwan@gmail.com'
EMAIL_PASSWORD = 'umslgdixngqoqcfd'  # Use an app password if using Gmail
SMTP_SERVER = 'smtp.mail.yahoo.com'
SMTP_PORT = 587

def get_rivn_price():
    url = f'https://finnhub.io/api/v1/quote?symbol={STOCK_SYMBOL}&token={FINNHUB_API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data['c']  # current price

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

def main_loop():
    last_price = None

    while True:
        try:
            current_price = get_rivn_price()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if current_price is None or current_price == 0:
                message = f"[{now}] RIVN current price: N/A"
            else:
                if last_price is not None:
                    percent_change = ((current_price - last_price) / last_price) * 100
                    change_str = f"{percent_change:+.2f}%"
                else:
                    change_str = "N/A (first reading)"

                message = (
                    f"[{now}]\n"
                    f"RIVN current price: ${current_price:.2f}\n"
                    f"Change since last hour: {change_str}"
                )
                last_price = current_price

            print(message)
            send_email(f"RIVN Price Update - {now}", message)

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(3600)  # Wait one hour

if __name__ == '__main__':
    main_loop()
