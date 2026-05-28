# Phase B Agent Prompt: Fix Mock Stack & Integration

You are an expert AI software architect and developer. Your objective is to debug, fix, and finalize a local integration pipeline that connects a stock data mock server to a local anonymization tool. The current baseline repository contains several intentional architectural and runtime bugs that you must resolve.

## Core Constraints & Safety Rules (CRITICAL)
- **Offline Only**: Do NOT put any external API URLs, remote Kafka configurations, or external services. All services must be bound to `127.0.0.1` or `localhost`.
- **No Secrets**: Do not generate, assume, or inject `.env` files, actual tokens, or passwords into any scripts. Only use the synthetic data in `mock/fixtures`.
- **Deterministic Anonymization**: The system uses `anonymizer/anonymize.py`. It is a local, rule-based text replacement tool. Do not add functional AI logic to intercept text at runtime.
- **Scope Limit**: Fix the bugs in `mock/`, `integration/`, and `tests/`. Refactor specifically to decouple hardcoded dependencies and apply KISS/DRY/SOLID principles, but do NOT rewrite the entire application from scratch. Be concise.

## Tech Stack & Commands
- **Language**: Python 3.11+
- **Frameworks**: FastAPI, `requests`, `pytest`, `uvicorn`
- **Install deps**: `pip install -r mock/server/requirements.txt`
- **Run the mock server**: `python mock/server/main.py`
- **Run tests**: `pytest integration/tests/`

---

## 🛠 Task Breakdown & Execution Plan

Please execute the following tasks sequentially:

### Task 1: Fix the Mock Data Server (`mock/server/main.py`)
1. **Path Resolution Bug**: The fixture loading path (`../fixtures/data.json`) assumes the script is run from a specific directory and fails during tests.
   - *Fix*: Use `__file__` (e.g., `os.path.join(os.path.dirname(__file__), "..", "fixtures", "data.json")`) to confidently resolve absolute paths relative to the current file.
2. **SSE Format Bug**: The `/api/stream` endpoint's `event_generator` simply yields JSON strings. 
   - *Fix*: Server-Sent Events (SSE) strictly require the lines to start with `data: `. Update the yield statement so it creates valid SSE frames (`yield f"data: {json.dumps(...)}\n\n"`).
3. **Port Mismatch**: The server is bound to port `8001`, but the client expects `8000`. 
   - *Fix*: Standardize the `uvicorn.run()` configuration to serve on port `8000`.

### Task 2: Robust Integration Pipeline (`integration/pipeline/run_pipeline.py`)
1. **Directory Availability Bug**: Writing to `out/un_anonymized.json` crashes if the `out/` folder does not exist.
   - *Fix*: Check for and securely create the `out/` directory using Python's `os.makedirs(..., exist_ok=True)` before trying to write to it.
2. **Anonymizer Integration**: Right now, the script fetches data but doesn't actually anonymize it.
   - *Fix*: Import or invoke the functionality from `anonymizer/anonymize.py` (which likely has file-to-file or JSON logic) so that right after saving `un_anonymized.json`, an `anonymized.json` file is also created where the fictional `trader_email` is masked.

### Task 3: Fix Flaky End-To-End Tests (`integration/tests/test_end_to_end.py`)
1. **Race Condition on Startup**: The system attempts to run tests milliseconds after calling `subprocess.Popen`, which crashes because the server process is still booting.
   - *Fix*: Implement a wait/retry mechanism (e.g., querying `http://127.0.0.1:8000/api/tickers` with a timeout and backoff) to strictly wait until the endpoint yields `200 OK` before testing the pipeline.
2. **Assertions Fix**: Verify that both `un_anonymized.json` and `anonymized.json` are successfully outputted to the `out/` folder and test file contents without rigidly assuming exact scalar values if possible, or assert existence and structural stability.

### Task 4: Documentation Logging
1. Update `documentation/ai-fix-log.md`:
   - Start your response by running the `pytest integration/tests/` to grab the failure logs. 
   - Once all logic is solid and the tests pass perfectly, write the final success output to `documentation/ai-fix-log.md`.
2. Ensure the top-level `README.md` correctly shows a human user how to launch everything sequentially or by running a single unifying script.

---

## Acceptance Criteria
- Running `pytest integration/tests/` yields a `100% PASS` with no race conditions.
- Running `python integration/pipeline/run_pipeline.py` successfully connects to `127.0.0.1:8000`, extracts data, and produces an anonymized file in `out/`.
- SSE events broadcast standard `data: ` strings.
- **Deliverable**: Everything runs flawlessly offline. Proceed by executing `pytest` first to prove the current broken state.
