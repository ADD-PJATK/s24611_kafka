import json
import time
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

TICKERS = ["AAPL", "MSFT", "GOOGL"]

def load_fixtures():
    # Intentionally bad path to string fixture loading
    with open('../fixtures/data.json') as f:
        return json.load(f)

@app.get("/api/tickers")
async def get_tickers():
    return TICKERS

@app.get("/api/latest")
async def get_latest(ticker: str):
    data = load_fixtures()
    # Bug: Assuming data has this structure without checking
    return data[ticker]

async def event_generator(ticker: str):
    data = load_fixtures()
    while True:
        # Deliberate SSE bug: missing 'data: ' prefix
        yield f"{json.dumps(data[ticker])}\n\n"
        await asyncio.sleep(1)

@app.get("/api/stream")
async def stream(ticker: str):
    return StreamingResponse(event_generator(ticker), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    # Deliberate bug: bind to wrong port where client doesn't look
    uvicorn.run(app, host="127.0.0.1", port=8001)
