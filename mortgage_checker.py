import requests
import os

# Config
FRED_API_KEY = os.getenv('FRED_API_KEY')
SERIES_ID = 'MORTGAGE30US'  # FRED series ID for 30yr fixed rate
THRESHOLD = 7.0  # TODO change later

# Telegram Config (optional)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_mortgage_rate():
    url = f'https://api.stlouisfed.org/fred/series/observations?series_id={SERIES_ID}&api_key={FRED_API_KEY}&file_type=json&sort_order=desc&limit=1'
    response = requests.get(url)
    data = response.json()
    return float(data['observations'][0]['value'])

def send_notification(rate):
    message = f"📉 Mortgage Rate Alert! 30-year fixed rate is {rate}% (below {THRESHOLD}%)"
    
    # Telegram Notification
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        requests.post(
            f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage',
            json={'chat_id': TELEGRAM_CHAT_ID, 'text': message}
        )

if __name__ == "__main__":
    try:
        current_rate = get_mortgage_rate()
        print(f"Current rate: {current_rate}%")
        
        if current_rate < THRESHOLD:
            send_notification(current_rate)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
