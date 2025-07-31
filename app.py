from flask import Flask, request, jsonify
from datetime import datetime
import requests
import re

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = '6430573316:AAHs_RBVflELPrEW-cxkeYJ04gA7H2LaRys'
TELEGRAM_CHAT_ID = '-1002885426467'  # or your chat ID
ZAPIER_WEBHOOK_URL = ''  # Optional

def format_chartink_data(raw_text):
    # Find all matches like "TICKER - 123.45"
    matches = re.findall(r'\b([A-Z]{2,})\s*-\s*[\d.]+', raw_text)
    tickers = [f"NSE:{ticker}" for ticker in matches]
    return ', '.join(tickers)

@app.route('/webhook/chartink', methods=['POST'])
def chartink_webhook():
    try:
        data = request.get_data(as_text=True)
        formatted = format_chartink_data(data)

        # Get current date and time in desired format
        now = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        
        # Send to Telegram
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        telegram_payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"Setup Stocks High EPS & RS - Equialpha\n{now}\n\n{formatted}"
        }
        requests.post(telegram_url, json=telegram_payload)

        # Optional: Send to Zapier
        if ZAPIER_WEBHOOK_URL:
            requests.post(ZAPIER_WEBHOOK_URL, json={"tickers": formatted})

        return jsonify({"status": "success", "formatted": formatted}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
