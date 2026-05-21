# App #2: History Downloader & Viewer

A data fetching and visualization tool for stock price history. Polls the Kafka API to collect historical data and provides table/chart views with CSV/JSON export capabilities.

## Features

- 📊 **Historical data fetching** - Polls `/api/latest` with configurable time ranges (1-10 minutes)
- 🎯 **Multi-ticker support** - Select multiple tickers at once using Ctrl+Click
- 📈 **Price charts** - Multi-ticker line charts for price trend visualization
- 📋 **Data tables** - Complete view of all fetched records with sorting capability
- 💾 **Export options** - Download data as CSV or JSON for external analysis
- 🔄 **Deduplication** - Automatically removes duplicate records (by ticker, timestamp, sequence)

## Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

## Installation

1. **Clone and navigate to the app directory:**
   ```bash
   cd app2-history-downloader
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
   http://localhost:5001
   ```

## Usage

1. **Select tickers:** Hold Ctrl and click multiple tickers or use Shift for ranges
2. **Set time range:** Choose duration in minutes (1-10, max API retention is ~10 min)
3. **Fetch data:** Click "📥 Fetch Data" button
4. **View results:** 
   - Chart shows price trends across selected tickers
   - Table displays all records with full details
5. **Export:**
   - **CSV**: For spreadsheet analysis (Excel, Google Sheets)
   - **JSON**: For programmatic processing or database import

## Time Range Considerations

- **API data retention:** ~10 minutes maximum
- **Polling interval:** 2 seconds (respects rate limit of 1 req/10s)
- **Max recommended:** 5-10 minutes gives good sample size
- **Min recommended:** 1-2 minutes for real-time data

## Data Export Format

### CSV
```
ticker,ts,price,currency,volume,seq
ACME,2026-05-07T15:30:00+02:00,123.45,PLN,1200,42
```

### JSON
```json
{
  "timestamp": "2026-05-07T15:35:20.123456",
  "record_count": 150,
  "data": [
    {
      "ticker": "ACME",
      "ts": "2026-05-07T15:30:00+02:00",
      "price": 123.45,
      "currency": "PLN",
      "volume": 1200,
      "seq": 42
    }
  ]
}
```

## API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `GET /api/tickers` | Fetch list of available 50 tickers |
| `GET /api/latest?ticker=ACME&ticker=BETA` | Fetch recent data for specific tickers |

## Backend Implementation

- **Server:** Flask (Python)
- **Polling:** 2-second intervals for up to specified duration
- **Deduplication:** By (ticker, timestamp, sequence) tuple
- **Authentication:** X-API-Key header
- **Sorting:** By ticker then timestamp

## Frontend Implementation

- **Framework:** Vanilla JavaScript + Chart.js
- **Multi-select:** Ctrl+Click support for ticker selection
- **Charts:** Multi-dataset line charts for comparison
- **Export:** Client-side generation for CSV/JSON downloads
- **Responsive:** Works on desktop and mobile

## Architecture Notes

- No database required - in-memory processing
- Polling-based collection respects API rate limits
- Automatic deduplication for clean data
- Sorted output for consistent analysis
- Memory efficient - streams data where possible

## Troubleshooting

**Issue:** "ERROR: ADD_API_KEY environment variable not set!"
- **Solution:** Ensure you've set the ADD_API_KEY before running the app

**Issue:** No data after fetching
- **Solution:** Check API is online; wait a few seconds for polling to complete

**Issue:** Fewer records than expected
- **Solution:** 
  - Ensure tickers are valid (check the list)
  - API may have limited data; try increasing duration
  - Check rate limits haven't been exceeded

**Issue:** Exported file is empty
- **Solution:** Ensure data was successfully fetched first; table should show records

## Rate Limits

- First 10 requests: Free
- After: Max 1 request / 10 seconds per API key

## License

Educational project - PJATK ADD
