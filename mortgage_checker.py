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
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(WEBSITE_URL, headers=headers)
        response.raise_for_status()
        
        # Print the HTML to debug
        print("Response status:", response.status_code)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try multiple approaches to find the rate
        
        # Approach 1: Look for elements with specific text patterns
        mortgage_elements = soup.find_all(['p', 'div', 'span', 'b'])
        for element in mortgage_elements:
            text = element.get_text().strip()
            if '30-year fixed' in text and '%' in text:
                print(f"Found potential element: {text}")
                import re
                rate_match = re.search(r'(\d+\.\d+)', text)
                if rate_match:
                    return float(rate_match.group(1))
        
        # Approach 2: Try to find rate in specific containers
        rate_containers = soup.select('._1bltAMwL._1zDr42Ck, ._1NFBFsHK')  # Common NerdWallet class names
        for container in rate_containers:
            text = container.get_text()
            if '%' in text and ('rate' in text.lower() or 'apr' in text.lower()):
                print(f"Found in container: {text}")
                import re
                rate_match = re.search(r'(\d+\.\d+)', text)
                if rate_match:
                    return float(rate_match.group(1))
        
        # Approach 3: Dump all percentage values found
        print("Attempting to find any percentage value...")
        import re
        for tag in soup.find_all(text=re.compile(r'\d+\.\d+%')):
            print(f"Found percentage: {tag.strip()}")
            rate_match = re.search(r'(\d+\.\d+)', tag.strip())
            if rate_match and '30' in tag.parent.get_text():
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
