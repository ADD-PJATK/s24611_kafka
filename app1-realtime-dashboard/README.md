# App #1: Realtime Stock Dashboard

A live stock price dashboard that connects to the Kafka SSE API and displays real-time price updates with interactive charts.

## Features

- 📡 **Live SSE streaming** - Real-time price updates from 50 companies
- 📊 **Interactive charts** - Chart.js visualization of price history (last 30 ticks)
- 🎯 **Multi-ticker support** - Subscribe to multiple tickers simultaneously
- 📈 **Price information** - Shows latest price, volume, timestamp, and currency
- 🎨 **Modern UI** - Responsive design with gradient theme

## Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

## Installation

1. **Clone and navigate to the app directory:**
   ```bash
   cd app1-realtime-dashboard
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Set up your API key:

**Option 1: Using `.env` file (recommended)**
```bash
cp .env.example .env
# Edit .env and add your API key:
ADD_API_KEY=your_key_here
```

**Option 2: Using environment variable (shell)**
```bash
export ADD_API_KEY=your_key_here    # macOS/Linux
set ADD_API_KEY=your_key_here       # Windows CMD
```

## How to Run

1. **Activate virtual environment (if created):**
   ```bash
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate        # Windows
   ```

2. **Start the Flask server:**
   ```bash
   python app.py
   ```

3. **Open in browser:**
   ```
   http://localhost:5000
   ```

## Usage

1. Open the dashboard in your browser
2. Select a ticker symbol from the dropdown (e.g., ACME, ALFA, BETA)
3. Click **Subscribe** to start receiving live updates
4. Multiple tickers can be subscribed to at once
5. Each ticker displays:
   - Real-time price chart (last 30 ticks)
   - Current price, timestamp, volume, and currency
   - Remove button to unsubscribe

## API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `GET /api/tickers` | Fetch list of available 50 tickers |
| `GET /api/stream?ticker=ACME` | Stream live ticks via SSE |

## Backend Implementation

- **Server:** Flask (Python)
- **Threading:** Background threads for each ticker stream
- **Data structure:** Deque (max 30 ticks per ticker)
- **Authentication:** X-API-Key header

## Frontend Implementation

- **Framework:** Vanilla JavaScript + Chart.js
- **Charts:** Line charts with real-time data updates
- **Polling:** Updates chart every 500ms
- **Responsive:** Works on desktop and mobile

## Architecture Notes

- No external database required - data stored in memory
- Each ticker runs in its own background thread
- Data updates are thread-safe using locks
- Graceful error handling for connection drops
- Easily scalable to more tickers

## Troubleshooting

**Issue:** "ERROR: ADD_API_KEY environment variable not set!"
- **Solution:** Ensure you've set the ADD_API_KEY before running the app

**Issue:** "Failed to fetch tickers"
- **Solution:** Check your API key is valid and the API service is accessible

**Issue:** No data appears in chart
- **Solution:** Wait a few seconds for data to arrive; ensure subscription was successful

## Rate Limits

- First 10 requests: Free
- After: Max 1 request / 10 seconds per API key

## License

Educational project - PJATK ADD
