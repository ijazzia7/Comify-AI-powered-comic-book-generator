from flask import Flask, render_template, jsonify
import requests, os

app = Flask(__name__)

def get_crypto_data():
    """Fetch cryptocurrency data from CoinGecko API"""
    # Get general market data (top 100 coins)
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 100,
        'page': 1,
        'sparkline': 'false',
        'price_change_percentage': '24h'
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Always fetch Vanar Chain (VANRY) separately
    vanry_url = "https://api.coingecko.com/api/v3/coins/vanar-chain"
    vanry_params = {
        "localization": "false",
        "tickers": "false",
        "market_data": "true",
        "community_data": "false",
        "developer_data": "false",
        "sparkline": "false"
    }
    v_res = requests.get(vanry_url, params=vanry_params, timeout=10)
    v_res.raise_for_status()
    v_data = v_res.json()

    vanry_entry = {
        'id': v_data['id'],  # should be "vanar-chain"
        'symbol': v_data['symbol'],  # "vanry"
        'name': v_data['name'],  # "Vanar Chain"
        'current_price': v_data['market_data']['current_price']['usd'],
        'price_change_percentage_24h': v_data['market_data']['price_change_percentage_24h'],
        'market_cap': v_data['market_data']['market_cap']['usd'],
        'image': v_data['image']['thumb'],
        'last_updated': v_data['last_updated']
    }

    # Ensure Vanar Chain is always the first item
    data.insert(0, vanry_entry)

    return data

def get_historical_data(coin_id):
    """Get historical price data for a specific coin"""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': 7,
        'interval': 'daily'
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()['prices']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cryptos')
def cryptos():
    try:
        data = get_crypto_data()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/<coin_id>')
def history(coin_id):
    try:
        data = get_historical_data(coin_id)
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Cloud Run provides PORT
    app.run(host="0.0.0.0", port=port)
