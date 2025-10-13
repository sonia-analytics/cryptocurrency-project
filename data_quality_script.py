import pandas as pd, os

CLEAN_DIR = "data/clean"
MASTER_FILE = os.path.join(CLEAN_DIR, "crypto_clean.csv")
REPORT_FILE = os.path.join(CLEAN_DIR, "data_quality_report.csv")

df = pd.read_csv(MASTER_FILE)

report = {
    "total_rows": len(df),
    "missing_values": df.isnull().sum().sum(),
    "duplicate_rows": df.duplicated().sum(),
    "invalid_prices": (df["current_price"] <= 0).sum(),
    "invalid_market_cap": (df["market_cap"] < 0).sum(),
}

pd.DataFrame([report]).to_csv(REPORT_FILE, index=False)
print("Data quality report saved:", REPORT_FILE)
pd.DataFrame([report])

REPORT_MD = os.path.join(CLEAN_DIR, "data_quality_report.md")

with open(REPORT_MD, "w", encoding="utf-8") as f:
    f.write("# Data Quality Report\n\n")
    for k, v in report.items():
        f.write(f"- **{k.replace('_', ' ').title()}**: {v}\n")

print("Markdown quality report saved:", REPORT_MD)