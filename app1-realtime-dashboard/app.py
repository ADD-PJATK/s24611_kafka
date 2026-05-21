#!/usr/bin/env python3
"""
Realtime Stock Dashboard - App #1
Connects to the Kafka SSE API and displays live price updates with charts.
"""
import os
import json
import requests
from flask import Flask, render_template, jsonify
from threading import Thread, Lock
from collections import defaultdict, deque
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
API_KEY = os.environ.get("ADD_API_KEY", "")
BASE_URL = "https://add.piotrkojalowicz.dev"
HEADERS = {"X-API-Key": API_KEY}

# Data storage: ticker -> deque of ticks (limited to 30 most recent)
price_history = defaultdict(lambda: deque(maxlen=30))
current_tickers = set()
data_lock = Lock()

# Available tickers (cached)
available_tickers = []


def fetch_tickers():
    """Fetch list of available tickers from API."""
    global available_tickers
    try:
        response = requests.get(f"{BASE_URL}/api/tickers", headers=HEADERS, timeout=5)
        response.raise_for_status()
        available_tickers = response.json().get("tickers", [])
        logger.info(f"Fetched {len(available_tickers)} tickers")
    except Exception as e:
        logger.error(f"Failed to fetch tickers: {e}")
        available_tickers = []


def stream_ticker(ticker):
    """Stream live data for a single ticker via SSE."""
    try:
        url = f"{BASE_URL}/api/stream"
        params = {"ticker": ticker}
        response = requests.get(
            url, params=params, headers=HEADERS, stream=True, timeout=30
        )
        response.raise_for_status()

        for line in response.iter_lines():
            if not line:
                continue
            
            line_str = line.decode("utf-8") if isinstance(line, bytes) else line
            
            # Parse SSE format: event: tick\ndata: {...}
            if line_str.startswith("data: "):
                try:
                    data = json.loads(line_str[6:])
                    with data_lock:
                        price_history[ticker].append(data)
                    logger.debug(f"Received tick for {ticker}: ${data.get('price')}")
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse JSON: {line_str}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Stream error for {ticker}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error streaming {ticker}: {e}")


@app.route("/")
def index():
    """Render the dashboard."""
    return render_template("index.html", tickers=available_tickers)


@app.route("/api/subscribe/<ticker>", methods=["POST"])
def subscribe(ticker):
    """Subscribe to a ticker's live updates."""
    ticker = ticker.upper()
    if ticker not in available_tickers:
        return jsonify({"error": "Invalid ticker"}), 400
    
    with data_lock:
        if ticker not in current_tickers:
            current_tickers.add(ticker)
            # Start streaming in background thread
            thread = Thread(target=stream_ticker, args=(ticker,), daemon=True)
            thread.start()
    
    return jsonify({"status": "subscribed", "ticker": ticker})


@app.route("/api/unsubscribe/<ticker>", methods=["POST"])
def unsubscribe(ticker):
    """Unsubscribe from a ticker."""
    ticker = ticker.upper()
    with data_lock:
        current_tickers.discard(ticker)
        # Keep history but stop streaming
    return jsonify({"status": "unsubscribed", "ticker": ticker})


@app.route("/api/data/<ticker>")
def get_data(ticker):
    """Get price history for a ticker."""
    ticker = ticker.upper()
    with data_lock:
        history = list(price_history.get(ticker, []))
    
    if not history:
        return jsonify({"ticker": ticker, "data": [], "latest": None})
    
    latest = history[-1]
    return jsonify({
        "ticker": ticker,
        "data": history,
        "latest": {
            "price": latest.get("price"),
            "timestamp": latest.get("ts"),
            "volume": latest.get("volume"),
            "currency": latest.get("currency"),
        }
    })


@app.route("/api/current-subscriptions")
def get_subscriptions():
    """Get currently subscribed tickers."""
    with data_lock:
        subs = list(current_tickers)
    return jsonify({"subscriptions": subs})


@app.errorhandler(500)
def handle_error(e):
    """Error handler."""
    logger.error(f"Server error: {e}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # Fetch tickers on startup
    fetch_tickers()
    
    if not API_KEY:
        print("ERROR: ADD_API_KEY environment variable not set!")
        print("Please set it before running: export ADD_API_KEY=<your_key>")
        exit(1)
    
    print(f"Starting Realtime Dashboard on http://localhost:5000")
    print(f"Loaded {len(available_tickers)} tickers")
    app.run(debug=False, host="0.0.0.0", port=5000, threaded=True)
