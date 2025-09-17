Tools:
Python + Jupyter Notebook, 
requests / API SDKs (data fetching), 
pandas (transformation & analysis), 
sqlite3,
schedule or APScheduler (automation)
logging (monitoring)
matplotlib / plotly (visualization)
streamlit (interactive dashboard),
pytest (testing pipeline functions), 
GitHub (repo, version control, portfolio)

# Cryptocurrency Project

**Author:** Sonia Mannepuli
**Date:** 9/14/2025

## Project Overview
This project is a Python-based ETL pipeline that collects cryptocurrency market data from the CoinGecko API.
It saves raw JSON/CSV snapshots with timestamps, cleans and transforms the data, and provides feature engineering for analysis.  
The pipeline demonstrates automation, data quality handling, and storage in multiple formats.

**Week 1!** - Setup & Extraction
- Dataset chosen: **Coin Gecko**
- Fetches ~900 crptocurriences 
- Save the JSON and the RAW with timestamp
- Saves cleaned CSV with selected columns
- Implemented retry logic for failed requests
- (Optional) Cleaned data was also stored locally on SQLite ('crypto_master.db') but is **not inmcluded in the repo** to keep it lightweight.

**Week2!** - Data Cleaning & Extraction
- Normalized column names (uppercase, lowercase)
- Handled missing values and duplictaes
- Added feature enginnering column: 'price_change_pct'
- Saved transformed dataset as CSV (with timestamp)

**Week3!** - Data Storage & Automation
- Stored cleaned data in:
  - **Master CSV** ('crypto_master.db'
-
-
-

Note:

## Files
- raw.csv - raw file with timestamp
- clean.csv = clean file with timestamp
- week_1.pynb
- week2.pynb
- raw.png - raw file with
- raw.json -

## Packages Intsalled
pip install pandas requests squlite

## Run dashboard locally
- streamlit run dashboard.py

## Live Demo
[Explore the live dashboard]()
    
## Example Visualizations

