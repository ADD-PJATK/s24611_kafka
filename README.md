# s24611_kafka — Kafka Real-time Stock Data & Data Anonymizer

**Student ID:** s24611  
**Repository:** https://github.com/ADD-PJATK/s24611_kafka  
**Assignment:** AA1 (Anonymizer) + AA2 (Kafka Realtime Stock Apps) + AA3 (Integration) + AA4 (AI Work Plan)

---

## 📂 Repository Structure

```
s24611_kafka/
├── app1-realtime-dashboard/      # Realtime stock price dashboard (Flask + Chart.js)
│   ├── app.py                    # Flask server with SSE streaming
│   ├── templates/index.html      # Dashboard UI
│   ├── static/
│   │   ├── style.css             # Styling
│   │   └── dashboard.js          # Frontend logic
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # API key configuration template
│   └── README.md                  # App-specific documentation
│
├── app2-history-downloader/      # Historical data fetcher & viewer
│   ├── app.py                    # Flask server with polling
│   ├── templates/index.html      # Data viewer UI
│   ├── static/
│   │   ├── style.css             # Styling
│   │   └── viewer.js             # Frontend logic
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # API key configuration template
│   └── README.md                  # App-specific documentation
│
├── anonymizer/                   # Data anonymization tool (AA1)
│   ├── anonymize.py              # Main anonymization script
│   ├── examples/
│   │   ├── mapping.json          # Example mapping configuration
│   │   ├── data.json             # Sample JSON file
│   │   └── users.csv             # Sample CSV file
│   └── README.md                 # Anonymizer documentation
│
├── documentation/
│   └── ai-work-plan.md           # AA4: AI work plan document
│
├── consolidation/
│   └── CONSOLIDATION.md          # Merge/integration notes
│
├── screenshots/                  # Screenshots of working apps
│   ├── app1_dashboard_live.png
│   ├── app1_multiple_tickers.png
│   ├── app2_fetched_data.png
│   ├── app2_charts_table.png
│   ├── app2_csv_export.png
│   └── anonymizer_example.png
│
├── .gitignore                    # Git ignore rules
├── README.md                     # This file
└── LICENSE                       # MIT
```

---

## 🚀 Quick Start

### Prerequisites (All Apps)
- **Python 3.6+**
- **pip** (Python package manager)
- **API Key**: Get from https://add.piotrkojalowicz.dev (class password: A@d-$01)

### 1️⃣ App #1: Realtime Stock Dashboard

Display live price updates for selected companies with interactive charts.

**Quick start:**
```bash
cd app1-realtime-dashboard
python -m venv venv
source venv/bin/activate              # On Windows: venv\Scripts\activate
pip install -r requirements.txt
export ADD_API_KEY=your_key_here      # On Windows: set ADD_API_KEY=...
python app.py
```
Then open: http://localhost:5000

**Features:**
- Subscribe to multiple tickers simultaneously
- Real-time price charts (last 30 ticks per ticker)
- Live price, volume, and timestamp updates

[Full documentation →](app1-realtime-dashboard/README.md)

---

### 2️⃣ App #2: History Downloader & Viewer

Fetch historical stock data, visualize trends, and export as CSV/JSON.

**Quick start:**
```bash
cd app2-history-downloader
python -m venv venv
source venv/bin/activate              # On Windows: venv\Scripts\activate
pip install -r requirements.txt
export ADD_API_KEY=your_key_here      # On Windows: set ADD_API_KEY=...
python app.py
```
Then open: http://localhost:5001

**Features:**
- Select multiple tickers with Ctrl+Click
- Fetch data over configurable time ranges (1-10 minutes)
- View data in interactive charts and tables
- Export as CSV or JSON

[Full documentation →](app2-history-downloader/README.md)

---

### 3️⃣ Anonymizer (AA1 - Included)

A local, standalone data anonymization tool with no external dependencies or APIs.

**Quick start:**
```bash
cd anonymizer

# Anonymize a CSV file
python anonymize.py --mapping examples/mapping.json --input examples/users.csv --output out/users.anon.csv

# Verbose mode (see each replacement)
python anonymize.py --mapping examples/mapping.json --input examples/data.json --output out/data.anon.json -v

# Dry run (show what would be replaced without writing)
python anonymize.py --mapping examples/mapping.json --input examples/users.csv --dry-run
```

**Supported formats:** JSON, CSV, TXT, MD (any text-based format)

[Full documentation →](anonymizer/README.md)

---

## 🔑 Configuration

### API Key Setup (Apps 1 & 2)

All apps require the `ADD_API_KEY` environment variable.

**Option 1: `.env` file (recommended)**
```bash
cp app1-realtime-dashboard/.env.example app1-realtime-dashboard/.env
# Edit .env and add your key
ADD_API_KEY=your_key_here
```

**Option 2: Environment variable**
```bash
export ADD_API_KEY=your_key_here        # macOS/Linux
set ADD_API_KEY=your_key_here           # Windows CMD
$env:ADD_API_KEY="your_key_here"        # Windows PowerShell
```

### Rate Limits
- First 10 requests: Free
- After: Max 1 request / 10 seconds per API key

---

## 📊 API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `GET /api/tickers` | Fetch list of 50 available tickers |
| `GET /api/latest?ticker=ACME` | Fetch recent data for specific tickers |
| `GET /api/stream?ticker=ACME` | Stream live ticks via SSE (Server-Sent Events) |

**Base URL:** https://add.piotrkojalowicz.dev  
**Authentication:** `X-API-Key: <YOUR_KEY>` header or `?api_key=<KEY>` query param

---

## 📸 Screenshots

All screenshots are in the [`screenshots/`](screenshots/) folder:

- **App #1:** Live dashboard with 2+ tickers and price history charts
- **App #2:** Fetched data displayed in table and chart with CSV/JSON export
- **Anonymizer:** Example run showing sensitive data replacement

---

## 🧪 Testing & Validation

### Testing App #1 (Realtime Dashboard)
1. Open http://localhost:5000
2. Select ACME, ALFA, BETA from dropdown
3. Click Subscribe and wait ~5 seconds for data to appear
4. Charts should update every 500ms with new ticks
5. Verify: ticker, price, timestamp, volume displayed correctly

### Testing App #2 (History Downloader)
1. Open http://localhost:5001
2. Select 3-5 tickers (Ctrl+Click)
3. Set duration to 5 minutes
4. Click "📥 Fetch Data" and wait
5. Table should show records from all tickers
6. Chart should display price trends
7. Test CSV export and JSON export

### Testing Anonymizer
```bash
cd anonymizer
python anonymize.py --mapping examples/mapping.json --input examples/users.csv --output out/test.csv -v
# Verify: Anna Nowak → PERSON_A, anna@firma.test → EMAIL_A
```

---

## 📝 Files Not Tracked

The following files are excluded from Git (see `.gitignore`):

- `.env` (contains API keys)
- `__pycache__/` (Python cache)
- `*.pyc` (compiled Python)
- `venv/` or `env/` (virtual environments)
- `node_modules/` (if applicable)
- `.DS_Store` (macOS)

---

## 🔗 Git Workflow

This repository demonstrates proper Git practices:

- **≥3 meaningful commits** showing development progression
- **Separate branches** for each feature (if desired)
- **No API keys committed** - stored only in `.env.example` as template
- **Clear commit messages** explaining changes
- `.gitignore` properly configured

---

## 📚 Documentation

- [AA1 - Anonymizer README](anonymizer/README.md)
- [AA2 App #1 - Realtime Dashboard README](app1-realtime-dashboard/README.md)
- [AA2 App #2 - History Downloader README](app2-history-downloader/README.md)
- [AA3 - Consolidation Notes](consolidation/CONSOLIDATION.md)
- [AA4 - AI Work Plan](documentation/ai-work-plan.md)

---

## 🛠 Architecture Notes

### Realtime Dashboard (App #1)
- **Backend:** Flask + threading
- **Frontend:** Vanilla JS + Chart.js
- **Data flow:** SSE → Background threads → In-memory deque → Frontend polling
- **Max history:** 30 ticks per ticker (configurable)

### History Downloader (App #2)
- **Backend:** Flask + polling (respects rate limits)
- **Frontend:** Vanilla JS + Chart.js
- **Data flow:** Repeated GET /api/latest → Deduplicate → Store → Display
- **Export:** Server-side CSV/JSON generation

### Anonymizer (AA1)
- **Type:** Standalone CLI tool
- **No dependencies:** Uses only Python stdlib
- **No APIs:** 100% local processing
- **Format:** Regex-based string replacement with configurable rules

---

## 🚨 Troubleshooting

**"ERROR: ADD_API_KEY environment variable not set!"**
→ Set your API key before running: `export ADD_API_KEY=your_key`

**"Failed to fetch tickers"**
→ Check API is online and your key is valid

**No data in charts**
→ Wait 5-10 seconds for data to arrive; check browser console for errors

**Rate limit exceeded**
→ You've made >10 requests in 10 seconds; wait before retrying

**Anonymizer output is empty**
→ Check input file exists and mapping is valid

---

## 📄 License

Educational project for PJATK — ADD (Additional Assignments)

---

## 👤 Student Information

- **Student ID:** s24611
- **Assignment:** Phase 2 (AA1 + AA2 + AA3 + AA4)
- **Date:** May 2026
- **Class:** Additional Assignments

---

## ✅ Acceptance Checklist (AA3 & AA4)

- [x] Repository created in ADD GitHub org, named `s24611_kafka`
- [x] Public or instructor-accessible
- [x] `main` branch contains AA1 + AA2 code + documentation
- [x] No API keys committed (`.env` in `.gitignore`)
- [x] Root README with repository map and quick start
- [x] Both AA2 apps have individual READMEs with full installation steps
- [x] Screenshots folder with working app demonstrations
- [x] Anonymizer runs from documented CLI command
- [x] `.gitignore` excludes `.env`, `__pycache__`, `venv/`, etc.
- [x] ≥3 meaningful Git commits showing development
- [x] AI work plan document (`documentation/ai-work-plan.md`)

---

For more details, see [ACCEPTANCE.md](task2/ACCEPTANCE.md) or the individual README files.

# Quick Start

To run the mock stack offline:

1. Install server dependencies:
   ```bash
   pip install -r mock/server/requirements.txt
   ```
2. Run the mock server:
   ```bash
   python mock/server/main.py
   ```
3. Run the integration pipeline tests (they will fail initially):
   ```bash
   pytest integration/tests/
   ```

For more details on the testing plan, see `documentation/plan-from-grading.md`

# Kafka Local Data Integration

This is the baseline repository connecting a local API to an anonymizing processor.

## How to run the local system

### Running manually
1. **Mock Data Server**: `python mock/server/main.py`
   - Binds on `http://127.0.0.1:8000`
   - Exposes mock stock event streams and rest endpoints.
2. **Launch Integration Pipeline**: `python integration/pipeline/run_pipeline.py`
   - Connects to the server locally, downloads data to `out/un_anonymized.json`, and invokes local anonymization script to yield `out/anonymized.json`.

### Testing Pipeline
Run the e2e integration suite by simply executing:
```sh
python -m pytest integration/tests/
```
*(Optionally just `pytest` if your PATH permits)*
