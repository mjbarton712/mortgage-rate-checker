# Mortgage Rate Checker 🏠📉

A GitHub-powered bot that monitors 30-year fixed mortgage rates and sends alerts when rates drop below a specified threshold.

[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/mjbarton712/mortgage-rate-checker/check_rate.yml?label=Rate%20Check)](https://github.com/mjbarton712/mortgage-rate-checker/actions)

---

## Features ✨
- Weekly rate checks using FRED Economic Data
- Telegram/Email notifications when rates drop below the threshold
- Error handling and data validation
- Free to run using GitHub Actions
- Easy configuration via environment variables

---

## Prerequisites 📋
- GitHub account
- [FRED API Key](https://research.stlouisfed.org/useraccount/apikeys)
- [Telegram Bot Token](https://core.telegram.org/bots#6-botfather) (optional)
- Python 3.10+

---

## Setup Instructions 🛠️

### 1. Clone Repository
```bash
git clone https://github.com/mjbarton712/mortgage-rate-checker.git
cd mortgage-rate-checker
```

### 2. Configure Secrets
Add these secrets in your GitHub repository Settings → Secrets → Actions:
- `FRED_API_KEY`: Your FRED API key
- `TELEGRAM_TOKEN` (optional): Telegram bot token from @BotFather
- `TELEGRAM_CHAT_ID` (optional): Your Telegram chat ID from @userinfobot

### 3. Customize Settings
Modify these values in `mortgage_checker.py`:
```python
THRESHOLD = 7.0  # Set your desired alert threshold
SERIES_ID = 'MORTGAGE30US'  # Change if monitoring a different rate
```

### 4. Schedule Configuration
The workflow is set to run every Thursday at 9 AM ET (14:00 UTC) by default. To modify:
```yaml
# In .github/workflows/check_rates.yml
schedule:
  - cron: '0 14 * * 4'  # UTC time format (minute hour day month day-of-week)
```

---

## Notification Setup 🔔

### Telegram Notifications
- Start a chat with `@mortgage_rate_butler_bot`
- Send `/start` to begin receiving alerts

### Email Notifications (Alternative)
- Add `SENDGRID_API_KEY` to GitHub Secrets
- Uncomment the email code in `send_notification()`
- Configure `from` and `to` emails in the code

---

## How It Works ⚙️
- Weekly API check via GitHub Actions
- Fetches the latest mortgage rate from FRED
- Compares against the threshold (currently 7.0%)
- Sends notifications if the rate drops below the threshold
- Full logs are available in the repository's Actions tab

---

## Customization Options 🎨
- **Multiple Recipients:** Add comma-separated chat IDs or emails
- **Different Rates:** Use alternative FRED series IDs:
  - 15-year fixed: `MORTGAGE15US`
  - 5/1 ARM: `MORTGAGE5US`
- **Notification Channels:** Add Slack/Discord webhooks
- **Threshold Adjustment:** Modify the `THRESHOLD` variable

---

## Troubleshooting 🐛
| Issue | Solution |
|-------|----------|
| KeyError: 'observations' | Check FRED API key validity |
| No valid mortgage rate | Expand the date range in `get_mortgage_rate()` |
| Notification failures | Verify Telegram credentials |
| Rate not updating | FRED updates Thursdays AM ET |

---

## License 📄
MIT License - See [LICENSE](./LICENSE) for details.

*Note: Mortgage rate data is provided by FRED® (Federal Reserve Economic Data) and may have a 1-week reporting delay. Always verify rates with official sources before making financial decisions.*

