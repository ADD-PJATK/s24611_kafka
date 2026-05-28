import requests

def fetch_latest_and_anonymize(ticker: str):
    # Bug: Server is actually running on 8001, not 8000
    r = requests.get(f"http://127.0.0.1:8000/api/latest?ticker={ticker}")
    r.raise_for_status()
    data = r.json()
    
    # Simple placeholder logic to write to output for anonymizer
    import json
    with open("out/un_anonymized.json", "w") as f:
        json.dump(data, f)
    
    return data
