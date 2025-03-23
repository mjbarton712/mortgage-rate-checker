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
    # Calculate date range (last 2 weeks to ensure we get data)
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d')
    
    url = f'https://api.stlouisfed.org/fred/series/observations?' \
          f'series_id={SERIES_ID}&' \
          f'api_key={FRED_API_KEY}&' \
          f'file_type=json&' \
          f'observation_start={start_date}&' \
          f'observation_end={end_date}&' \
          f'sort_order=desc'
    
    response = requests.get(url)
    data = response.json()
    
    print(f"DEBUG: API Response - {data}")  # Debugging line
    
    if 'observations' not in data or len(data['observations']) == 0:
        raise ValueError("No observations found in API response")
    
    # Find the first valid recent value (skip '.' placeholder values)
    for observation in data['observations']:
        value = observation.get('value', '')
        if value and value != '.':
            return float(value)
    
    raise ValueError("No valid mortgage rate found in observations")


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
