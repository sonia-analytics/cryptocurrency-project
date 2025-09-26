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
- **Master CSV** ('crypto_master.db', table: 'crypto')
- Wrote and tested sample SQL queries using `pandas.read_sql()` in Jupyter  
  > Note: DB Browser could not open the `.db` file, so queries were run directly in Python instead.
- Automated pipeline with the `schedule` library (runs daily at midnight)
- Added logging:
  - Run timestamp
  - Number of new rows added
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

## Files
- crypto_raw.csv - raw file with timestamp
- crypto_clean.csv = clean file with timestamp
- week_1.pynb - analysis noteboook for week 1
- week2.pynb - analyssis note
- crypto_raw.json - raw json file with timestamp

## Packages Intsalled
pip install pandas requests squlite schedule logging

## Run dashboard locally
- streamlit run dashboard.py

## Live Demo
[Explore the live dashboard]()
    
## Example Visualizations

