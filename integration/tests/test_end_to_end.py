import subprocess
import time
import os
import requests
import pytest

def wait_for_server():
    for _ in range(10):
        try:
            r = requests.get("http://127.0.0.1:8000/api/tickers")
            if r.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(0.5)
    return False

def test_pipeline_end_to_end():
    # Attempt to start the server in the background
    server_process = subprocess.Popen(["python", "mock/server/main.py"])

    try:
        # Wait for the server to be ready
        assert wait_for_server(), "Server failed to start in time"
        
        from integration.pipeline.run_pipeline import fetch_latest_and_anonymize
        # Trying to fetch AAPL
        data = fetch_latest_and_anonymize("AAPL")
        
        assert data is not None

        # Check files
        assert os.path.exists("out/un_anonymized.json")
        assert os.path.exists("out/anonymized.json")

    finally:
        server_process.terminate()
        server_process.wait()
