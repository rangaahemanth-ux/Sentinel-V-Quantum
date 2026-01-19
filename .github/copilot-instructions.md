# Copilot Instructions for Sentinel-V

Purpose: Help AI coding agents get productive quickly in this repo by summarizing the architecture, developer workflows, conventions, and concrete examples.

- **Big Picture**: The UI is a Streamlit front-end (`app.py`) that drives a small scanning engine in `core.py`. The user enters a domain in the UI; `Scanner.get_subdomains()` (async, uses `aiohttp` and crt.sh) returns subdomains which are analyzed by two synchronous methods (`calculate_risk`, `analyze_quantum_risk`). Results are built into two pandas DataFrames and merged on the `asset` field for display.

- **Key files**:
  - `app.py` — Streamlit UI, `st.session_state.audit_data` persists results.
  - `core.py` — `Scanner` class: `get_subdomains()` (async), `calculate_risk()`, `analyze_quantum_risk()`.
  - `requirements.txt` — runtime deps: `streamlit`, `pandas`, `aiohttp`, `fpdf`.

- **Why things are structured this way**:
  - Separation of concerns: `app.py` handles presentation and state; `core.py` implements network I/O and risk logic so it can be called from other contexts (CLI, tests, worker).
  - Async network calls are isolated inside `Scanner.get_subdomains()` using `aiohttp` to avoid blocking the Streamlit thread.

- **Data flow / contract to preserve**:
  - `Scanner.get_subdomains()` must return an iterable of strings (lowercased hostnames). `core.py` currently returns a fallback list on network error.
  - Both `calculate_risk()` and `analyze_quantum_risk()` return dicts that include an `asset` key — this is CRITICAL because `app.py` performs a pandas `merge` on `asset`.

- **Developer workflows (how to run & debug)**
  - Install deps (Windows):

    ```powershell
    py -3 -m pip install -r requirements.txt
    ```

  - Run the Streamlit UI:

    ```powershell
    streamlit run app.py
    ```

  - Quick debug of async scanner from the console:

    ```powershell
    py -3 -c "import asyncio; from core import Scanner; print(asyncio.run(Scanner('prosec-networks.com').get_subdomains()))"
    ```

- **Project-specific patterns & conventions**
  - Keep the `asset` key present and unique for each returned record: pandas merges depend on this.
  - `st.session_state.audit_data` stores the merged DataFrame. When altering output columns, update both `app.py` display columns and the DataFrame keys.
  - Network calls use `aiohttp` with a short timeout (12s) and fall back to `www.<domain>` on error — preserve that behavior unless you intentionally change UX for failed scans.

- **Integration & external dependencies**
  - Live dependency on `https://crt.sh` for subdomain discovery; changes in that service or rate-limiting will affect UX. Cache or rate-limit at the `Scanner` layer if adding heavier load.
  - No DB or background queue is present; results are ephemeral in Streamlit session state.

- **Safe modification checklist for PRs**
  - If changing `Scanner.get_subdomains()` output shape, update `calculate_risk()`/`analyze_quantum_risk()` and the `app.py` merge keys.
  - If adding columns to risk dicts, ensure display slices in `app.py` (e.g., `df[['asset','Quantum_Risk', ...]]`) are updated.
  - Keep async/sync boundaries clear: don't call `async` functions directly from synchronous code without using an event loop (see current pattern in `app.py`).

- **Examples**
  - Merge contract: both analyzers return `{'asset': <str>, '...': ...}` so that `pd.merge(df_c, df_q, on='asset')` works in `app.py`.

If anything here is unclear or you'd like the instructions to emphasize different workflows (CI, testing, packaging), tell me which areas to expand. I can iterate the file. 
