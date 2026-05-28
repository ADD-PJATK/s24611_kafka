import os
import json
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

app = FastAPI()

def load_fixtures():
    # Fix: Use __file__ to comfortably resolve the absolute path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fixtures_path = os.path.join(base_dir, "..", "fixtures", "data.json")
    with open(fixtures_path, 'r') as f:
        return json.load(f)

@app.get("/api/tickers")
async def get_tickers():
    data = load_fixtures()
    # Fix: Correctly get top-level keys
    return list(data.keys())

@app.get("/api/latest")
async def get_latest(ticker: str):
    data = load_fixtures()
    # Fix: Ensure logic looks at top-level instead of 'stocks' which isn't there
    if ticker not in data:
        raise HTTPException(status_code=404, detail="Ticker not found")
    
    return data[ticker]

@app.get("/api/stream")
async def stream_ticker(ticker: str):
    data = load_fixtures()
    if ticker not in data:
        raise HTTPException(status_code=404, detail="Ticker not found")

    async def event_generator():
        # Fix: For stream we just yield the single update or create fake updates 
        # based on data[ticker] over time if required.
        # However, for previous code we assume it's one item, but maybe it's not a list.
        update = data[ticker]
        for _ in range(5): # yield a few times for stream
            yield f"data: {json.dumps(update)}\n\n"
            await asyncio.sleep(0.5)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    # Fix: Change port to 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
