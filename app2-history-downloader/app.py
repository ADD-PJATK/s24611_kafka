#!/usr/bin/env python3
"""
History Downloader & Viewer - App #2
Fetches historical stock data and displays it as table/chart with CSV/JSON export.
"""
import os
import json
import csv
import requests
from flask import Flask, render_template, jsonify, request, send_file
from datetime import datetime, timedelta
from io import StringIO, BytesIO
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
API_KEY = os.environ.get("ADD_API_KEY", "")
BASE_URL = "https://add.piotrkojalowicz.dev"
HEADERS = {"X-API-Key": API_KEY}

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


def fetch_historical_data(tickers, duration_minutes=5):
    """
    Fetch historical data by polling /api/latest at regular intervals.
    Since data is retained for ~10 minutes, we'll do polling with 2s intervals.
    """
    tickers = [t.upper() for t in tickers if t]
    if not tickers:
        return []

    all_data = []
    start_time = datetime.now()
    
    # Poll for the specified duration
    while (datetime.now() - start_time).total_seconds() < duration_minutes * 60:
        try:
            params = {"ticker": tickers}
            response = requests.get(
                f"{BASE_URL}/api/latest",
                params=params,
                headers=HEADERS,
                timeout=5
            )
            response.raise_for_status()
            
            data = response.json().get("data", [])
            all_data.extend(data)
            logger.info(f"Fetched {len(data)} records for {len(tickers)} tickers")
            
            # Wait 2 seconds before next poll (rate limit: 1 request per 10s, but we can do 5 in advance)
            import time
            time.sleep(2)
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            break
    
    # Deduplicate by (ticker, ts, seq)
    seen = set()
    unique_data = []
    for record in all_data:
        key = (record.get("ticker"), record.get("ts"), record.get("seq"))
        if key not in seen:
            seen.add(key)
            unique_data.append(record)
    
    # Sort by ticker, then by timestamp
    unique_data.sort(key=lambda x: (x.get("ticker", ""), x.get("ts", "")))
    
    return unique_data


@app.route("/")
def index():
    """Render the history viewer."""
    return render_template("index.html", tickers=available_tickers)


@app.route("/api/fetch-history", methods=["POST"])
def fetch_history():
    """Fetch historical data for selected tickers."""
    data = request.get_json()
    tickers = data.get("tickers", [])
    duration = int(data.get("duration", 5))  # minutes
    
    if not tickers:
        return jsonify({"error": "No tickers selected"}), 400
    
    if duration < 1 or duration > 10:
        return jsonify({"error": "Duration must be 1-10 minutes"}), 400
    
    try:
        historical_data = fetch_historical_data(tickers, duration)
        return jsonify({
            "status": "success",
            "count": len(historical_data),
            "data": historical_data,
            "tickers": tickers,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error in fetch_history: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/export-csv", methods=["POST"])
def export_csv():
    """Export data as CSV."""
    data = request.get_json()
    records = data.get("data", [])
    
    if not records:
        return jsonify({"error": "No data to export"}), 400
    
    try:
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "ticker", "ts", "price", "currency", "volume", "seq"
        ])
        writer.writeheader()
        writer.writerows(records)
        
        # Convert to bytes
        csv_bytes = BytesIO(output.getvalue().encode('utf-8'))
        csv_bytes.seek(0)
        
        filename = f"stock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        return send_file(
            csv_bytes,
            mimetype="text/csv",
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logger.error(f"Error exporting CSV: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/export-json", methods=["POST"])
def export_json():
    """Export data as JSON."""
    data = request.get_json()
    records = data.get("data", [])
    
    if not records:
        return jsonify({"error": "No data to export"}), 400
    
    try:
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "record_count": len(records),
            "data": records
        }
        
        json_bytes = BytesIO(json.dumps(export_data, indent=2).encode('utf-8'))
        json_bytes.seek(0)
        
        filename = f"stock_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        return send_file(
            json_bytes,
            mimetype="application/json",
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logger.error(f"Error exporting JSON: {e}")
        return jsonify({"error": str(e)}), 500


@app.errorhandler(500)
def handle_error(e):
    """Error handler."""
    logger.error(f"Server error: {e}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    fetch_tickers()
    
    if not API_KEY:
        print("ERROR: ADD_API_KEY environment variable not set!")
        print("Please set it before running: export ADD_API_KEY=<your_key>")
        exit(1)
    
    print(f"Starting History Downloader on http://localhost:5001")
    print(f"Loaded {len(available_tickers)} tickers")
    app.run(debug=False, host="0.0.0.0", port=5001, threaded=True)
