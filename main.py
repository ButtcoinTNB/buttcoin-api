from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

COINGECKO_MEMECOIN_URL = "https://api.coingecko.com/api/v3/coins/categories/meme-token"
COINGECKO_BUTTCOIN_URL = "https://api.coingecko.com/api/v3/coins/buttcoin-4"

def fetch_data(url):
    for attempt in range(3):
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"Rate limit hit. Retrying in {10 * (attempt + 1)} seconds...")
            time.sleep(10 * (attempt + 1))
    return None

@app.route('/')
def home():
    return "API is running! Use /fetch to get data."

@app.route('/fetch', methods=['GET'])
def fetch_coingecko_data():
    memecoin_data = fetch_data(COINGECKO_MEMECOIN_URL)
    buttcoin_data = fetch_data(COINGECKO_BUTTCOIN_URL)

    if not memecoin_data or not buttcoin_data:
        return jsonify({"error": "Failed to fetch data"}), 500

    result = {
        "memecoin_market_cap": memecoin_data.get("market_cap"),
        "buttcoin_price": buttcoin_data.get("market_data", {}).get("current_price", {}).get("usd")
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)