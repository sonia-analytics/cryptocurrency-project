import requests, pandas as pd, os, json, sqlite3
from datetime import datetime, timezone
from time import sleep

ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
RAW_DIR, CLEAN_DIR = "data/raw","data/clean"
MASTER_DB = os.path.join(CLEAN_DIR,"crypto_master.db")
for d in [RAW_DIR,CLEAN_DIR]: os.makedirs(d,exist_ok=True)

def fetch_crypto(pages=5,retries=3):
    data=[]
    for p in range(1,pages+1):
        for i in range(retries):
            try:
                r=requests.get(
                    "https://api.coingecko.com/api/v3/coins/markets",
                    params={"vs_currency":"usd","order":"market_cap_desc",
                            "per_page":250,"page":p,"sparkline":"false"},timeout=15)
                r.raise_for_status()
                page_data=r.json()
                for item in page_data: item["fetched_at"]=ts
                data.extend(page_data)
                break
            except: sleep(2**i)
    df = pd.DataFrame(data).drop_duplicates(subset="id").head(900)
    return df

cleaned = fetch_crypto()
cleaned.to_csv(f"{RAW_DIR}/crypto_raw_{ts}.csv",index=False)
with open(f"{RAW_DIR}/crypto_raw_{ts}.json","w",encoding="utf-8") as f:
    json.dump(cleaned.to_dict(orient="records"),f,indent=2)

fields=["id","symbol","name","current_price","market_cap","total_volume",
        "high_24h","low_24h","price_change_percentage_24h","fetched_at"]
cleaned[fields].to_csv(f"{CLEAN_DIR}/crypto_clean_{ts}.csv",index=False)

conn=sqlite3.connect(MASTER_DB)
conn.execute("DROP TABLE IF EXISTS crypto")
cleaned[fields].to_sql("crypto",conn,if_exists="replace",index=False)
conn.close()
print(f"Week 1 complete: {len(cleaned)} rows saved")
