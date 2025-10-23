import pandas as pd
import numpy as np
import os

RAW_DIR, CLEAN_DIR = "data/raw","data/clean"
ts = "20250914T020336Z" 
raw_file = f"{RAW_DIR}/crypto_raw_{ts}.csv"

df = pd.read_csv("data/raw/crypto_raw.csv")

df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]

df.drop_duplicates(subset="id", inplace=True)
df.fillna(0, inplace=True)  

#Feature engineering
df["price_change_pct"] = df["price_change_percentage_24h"].fillna(0)

fields = ["id","symbol","name","current_price","market_cap","total_volume",
          "high_24h","low_24h","price_change_pct","fetched_at"]
df[fields].to_csv(f"{CLEAN_DIR}/crypto_clean_{ts}.csv", index=False)

print(f"Week 2 complete: {len(df)} rows cleaned & transformed")