from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = '6430573316:AAHs_RBVflELPrEW-cxkeYJ04gA7H2LaRys'
TELEGRAM_CHAT_ID = '-1002885426467'  # or your chat ID
ZAPIER_WEBHOOK_URL = ''  # Optional

def format_chartink_data(raw_text):
    lines = raw_text.strip().split('\n')
    tickers = []
    for line in lines:
        match = re.match(r'^([A-Z]+)\s*-\s*\d+', line.strip())
        if match:
            tickers.append(f"NSE:{match.group(1)}")
    return ', '.join(tickers)

@app.route('/webhook/chartink', methods=['POST'])
def chartink_webhook():
    try:
        data = request.get_data(as_text=True)
        formatted = format_chartink_data(data)

        # Send to Telegram
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        telegram_payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": f"Formatted Tickers: {formatted}"
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
