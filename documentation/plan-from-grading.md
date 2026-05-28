# Phase 2 Plan (from Grading)

## Summary of Phase 2 Feedback
My integration had several issues, mostly with hardcoded paths causing the anonymizer to fail when run from different directories. Tests were flaky because they didn't properly wait for the backend to start. 

## Mock / Test Plan
1. **Mock Server**: I will build a local FastAPI mock that returns synthetic tickers, latest prices, and streaming SSE.
2. **Integration Pipeline**: A basic Python script that queries the mock and stores data inside `out/`.
3. **Tests**: A pytest end-to-end test that spins up the mock server, runs the query, and verifies output.

## Anticipated Failure Modes (Intentional Bugs introduced for Phase B)
1. **Race Condition**: `test_end_to_end.py` starts the server and immediately queries it without waiting.
2. **Port Mismatch**: `run_pipeline.py` queries port `8000`, but `main.py` starts the server on port `8001`.
3. **Path Resolution Bug**: `main.py` uses `../fixtures/data.json` instead of a stable root-relative or absolute path, causing file not found errors depending on `pwd`.
4. **SSE Format Bug**: `main.py` `event_generator` sends regular JSON instead of preceding it with `data: `, violating the SSE protocol.
5. **Missing output directory**: `run_pipeline.py` writes to `out/un_anonymized.json`, but the `out/` directory might not exist.
