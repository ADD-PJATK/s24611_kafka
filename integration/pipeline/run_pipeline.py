import requests
import json
import os
import subprocess

def fetch_latest_and_anonymize(ticker: str):
    r = requests.get(f"http://127.0.0.1:8000/api/latest?ticker={ticker}")
    r.raise_for_status()

    # Ensure out directory exists
    os.makedirs("out", exist_ok=True)

    un_anonymized_path = "out/un_anonymized.json"
    anonymized_path = "out/anonymized.json"

    with open(un_anonymized_path, "w") as f:
        json.dump(r.json(), f)

    # Anonymize using subprocess
    mapping_path = os.path.join("anonymizer", "examples", "mapping.json")
    subprocess.run([
        "python", "anonymizer/anonymize.py",
        "--mapping", mapping_path,
        "--input", un_anonymized_path,
        "--output", anonymized_path
    ], check=True)
    
    return r.json()

if __name__ == "__main__":
    fetch_latest_and_anonymize("AAPL")
