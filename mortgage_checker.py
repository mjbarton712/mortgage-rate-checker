import os
import requests
import smtplib
from email.message import EmailMessage
from datetime import datetime
from requests_html import HTMLSession

WEBSITE_URL = "https://www.nerdwallet.com/mortgages/mortgage-rates"
TARGET_RATE = 7.0  # TODO update to be lower - it is high for testing functionality.
SMTP_SERVER = "smtp.gmail.com"  # SMTP specific to gmail - other providers would be diff
SMTP_PORT = 587

from requests_html import HTMLSession

WEBSITE_URL = "https://www.nerdwallet.com/mortgages/mortgage-rates"

def get_rate():
    try:
        session = HTMLSession()
        response = session.get(WEBSITE_URL)
        response.html.render(timeout=20)

        # Check the page content to ensure it's loading correctly
        print(response.html.html[:1000])  # Print the first 1000 characters for debugging

        # Try more specific selectors or keyword search
        rate_element = response.html.find('div[data-testid="30year-fixed-rate"] span', first=True)

        if rate_element:
            rate_text = rate_element.text.strip()
            import re
            rate_match = re.search(r'(\d+\.\d+)', rate_text)
            if rate_match:
                return float(rate_match.group(1))

        return None
    except Exception as e:
        print(f"Error getting rate: {e}")
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
