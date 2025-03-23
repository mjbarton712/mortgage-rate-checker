import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import datetime

WEBSITE_URL = "https://www.nerdwallet.com/mortgages/mortgage-rates"
TARGET_RATE = 7.0  # TODO update to be lower - it is high for testing functionality.
SMTP_SERVER = "smtp.gmail.com"  # SMTP specific to gmail - other providers would be diff
SMTP_PORT = 587

def get_rate():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(WEBSITE_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # The current xpath (subject to change) is /html/body/div[2]/div[2]/div/p/b
    rate_element = soup.select_one('html > body > div:nth-of-type(2) > div:nth-of-type(2) > div > p > b')
    
    if rate_element:
        rate_text = rate_element.get_text().strip()
        # Extract the rate number from the text
        rate = ''.join(filter(lambda x: x.isdigit() or x == '.', rate_text))
        return float(rate)
    return None

def send_notification(current_rate):
    msg = EmailMessage()
    msg.set_content(f"30-year mortgage rate is now {current_rate}%!\nCheck it out: {WEBSITE_URL}")
    
    msg['Subject'] = f"Mortgage Rate Alert: {current_rate}%!"
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = os.getenv('EMAIL_USER')
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))
        server.send_message(msg)

if __name__ == "__main__":
    current_rate = get_rate()
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - Current rate: {current_rate}%")
    
    if current_rate and current_rate < TARGET_RATE:
        print("Rate below threshold! Sending notification...")
        send_notification(current_rate)
    else:
        print("Rate above threshold - no action needed")
