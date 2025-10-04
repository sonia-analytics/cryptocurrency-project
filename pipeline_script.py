import os, sqlite3, logging, pandas as pd
from glob import glob
from datetime import datetime
from time import sleep
import schedule

CLEAN_DIR, MASTER_CSV, MASTER_DB = "crypto_clean.csv","crypto_master.csv","crypto_master.db"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/week3.log", level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s")

def latest_clean():
    files = glob(os.path.join(CLEAN_DIR, "crypto_clean*.csv"))
    return max(files, key=os.path.getmtime) if files else None

def job():
    try:
        src = latest_clean()
        if not src: return logging.info("No cleaned CSV found.")
        df_new = pd.read_csv(src)
        if os.path.exists(MASTER_CSV): master = pd.read_csv(MASTER_CSV)
        else: master = pd.DataFrame(columns=df_new.columns)
        before = len(master)
        master = pd.concat([master, df_new]).drop_duplicates(subset=["id","fetched_at"])
        master.to_csv(MASTER_CSV, index=False)
        sqlite3.connect(MASTER_DB).cursor().execute("DROP TABLE IF EXISTS crypto")
        with sqlite3.connect(MASTER_DB) as conn:
            master.to_sql("crypto", conn, if_exists="replace", index=False)
        added = len(master) - before
        logging.info(f"SUCCESS: {added} new rows from {os.path.basename(src)}")
    except Exception as e:
        logging.exception(f"ERROR: {e}")

schedule.every().day.at("00:00").do(job)

if __name__ == "__main__":
    job()
    while True:
        schedule.run_pending(); sleep(30)