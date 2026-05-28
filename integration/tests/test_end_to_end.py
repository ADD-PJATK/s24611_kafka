import pytest
import os
import requests
import subprocess
import time

def test_pipeline_end_to_end():
    # Attempt to start the server in the background
    server_process = subprocess.Popen(["python", "mock/server/main.py"])
    
    # Bug: Race condition! Not waiting for the server to spin up
    
    try:
        from integration.pipeline.run_pipeline import fetch_latest_and_anonymize
        # Trying to fetch AAPL
        data = fetch_latest_and_anonymize("AAPL")
        
        # Test checks if a file was created
        assert os.path.exists("out/un_anonymized.json")
        
        # Bug: Bad assert based on fixture content
        assert data["price"] == 150.0
        assert data["trader_email"] == "john.doe@example.com"
        
    finally:
        server_process.terminate()
        server_process.wait()
