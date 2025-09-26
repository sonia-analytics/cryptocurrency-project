# Cryptocurrency Project

**Author:** Sonia Mannepuli
**Date:** September 2025

## Project Overview
This project  builds a Python-based ETL pipeline that collects cryptocurrency market data from the **CoinGecko API**, saves raw snapshots (CSV/JSON), cleans and transforms the data, and stores it in **SQLite** for analysis. The project demonstrates automation, logging, and reproducible data workflows.

**Week 1!** - Setup & Extraction
 Dataset chosen: **Cryptocurrency (CoinGecko API)**s** with timestamps
- Python script fetches ~900 top coins
- Saves raw **CSV + JSON snapshot
- Implements retry logic for failed API requests

**Week2!** - Data Cleaning & Extraction
- Normalized column names (lowercase, underscores)
- Removed duplicates and handled missing values
- Added feature: `price_change_pct`
- Saved cleaned dataset (`crypto_clean_*.csv`)
- Unit tests (`pytest`) verify:
  - No duplicate IDs
  - No missing prices
 
**Week3!** - Data Storage & Automation
-- Stored cleaned data in:
  - Master CSV (`crypto_master.csv`)
  - SQLite database (`crypto_master.db`, table: `crypto`)
- Verified using sample SQL queries in Jupyter:
  ```sql
  SELECT COUNT(*) FROM crypto;
  SELECT id, name, current_price, market_cap FROM crypto ORDER BY market_cap DESC LIMIT 5;
  ```
- Automated with `schedule` (daily at midnight + immediate run)
- Logging records:
  - Timestamp
  - Rows added
  - Errors (if any)

Example log entry:
2025-09-17 14:21:08,752 INFO SUCCESS: 0 new rows from crypto_clean.csv

## Database Storage
SQlite ('squlite3') was used to store sucessfully to store the cleaned cryptocurrency dataset.
The pipeline connects to a local SQLite database (`crypto_master.db`)
- The cleaned data is written into a table called `crypto`
- Each run updates the master dataset with new rows
- The database can be queried directly with `sqlite3` or via pandas in Jupyter

> Note: PostgreSQL was optional in the rubric. For this project, SQLite was sufficient and fully implemented.

## Project Structure
- `data/raw/` → raw JSON + CSV snapshots
- `data/clean/` → cleaned CSV, master CSV, SQLite DB
- `scripts/` → pipeline scripts (`fetch_crypto.py`, `clean_crypto.py`, `automate_pipeline.py`)
- `notebooks/` → interactive Jupyter notebooks
- `docs/` → pipeline architecture diagram
- `logs/` → pipeline run logs
- 
## Packages Intsalled
pip install pandas requests squlite schedule logging

## Running the Pipeline
```bash
python scripts/fetch_crypto.py   # Fetch raw + clean data
python scripts/clean_crypto.py   # Transform data
python scripts/automate_pipeline.py  # Daily scheduled run with logging
```
## Run dashboard locally
- streamlit run dashboard.py

## Live Demo
[Explore the live dashboard]()
    
## Example Visualizations

