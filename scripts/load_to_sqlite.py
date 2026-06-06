import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR  = Path(__file__).resolve().parent.parent
PROCESSED = BASE_DIR / "data" / "processed"
DB_PATH   = BASE_DIR / "data" / "db" / "bluestock_mf.db"

print("\n🚀 SQLITE LOADING STARTED\n")

conn = sqlite3.connect(DB_PATH)

# DIM_FUND
fund = pd.read_csv(BASE_DIR / "data" / "raw" / "01_fund_master.csv")
fund.columns = fund.columns.str.strip().str.lower()
fund = fund.rename(columns={"scheme_name": "fund_name", "amc": "fund_house", "risk_grade": "risk_level"})
fund = fund[[c for c in ["amfi_code","fund_name","fund_house","category","sub_category","risk_level"] if c in fund.columns]]
conn.execute("DROP TABLE IF EXISTS dim_fund")
fund.to_sql("dim_fund", conn, if_exists="replace", index=False)
print("✅ dim_fund:", len(fund))

# DIM_DATE
nav_dates = pd.read_csv(PROCESSED / "nav_clean.csv", usecols=["date"])
txn_dates = pd.read_csv(PROCESSED / "transactions_clean.csv", usecols=["transaction_date"])
txn_dates.columns = ["date"]
all_dates = pd.concat([nav_dates, txn_dates]).drop_duplicates()
all_dates["date"] = pd.to_datetime(all_dates["date"])
all_dates = all_dates.sort_values("date")
dim_date = pd.DataFrame({
    "date":    all_dates["date"].dt.strftime("%Y-%m-%d"),
    "year":    all_dates["date"].dt.year,
    "month":   all_dates["date"].dt.month,
    "day":     all_dates["date"].dt.day,
    "quarter": all_dates["date"].dt.quarter
})
conn.execute("DROP TABLE IF EXISTS dim_date")
dim_date.to_sql("dim_date", conn, if_exists="replace", index=False)
print("✅ dim_date:", len(dim_date))

# FACT_NAV
nav = pd.read_csv(PROCESSED / "nav_clean.csv")
conn.execute("DROP TABLE IF EXISTS fact_nav")
nav.to_sql("fact_nav", conn, if_exists="replace", index=False)
print("✅ fact_nav:", len(nav))

# FACT_TRANSACTIONS
txn = pd.read_csv(PROCESSED / "transactions_clean.csv")
txn = txn.rename(columns={"transaction_date": "date", "amount_inr": "amount", "state": "investor_state"})
txn["units"] = 0
txn = txn[[c for c in ["amfi_code","date","transaction_type","amount","units","investor_state","kyc_status"] if c in txn.columns]]
conn.execute("DROP TABLE IF EXISTS fact_transactions")
txn.to_sql("fact_transactions", conn, if_exists="replace", index=False)
print("✅ fact_transactions:", len(txn))

# FACT_PERFORMANCE
perf = pd.read_csv(PROCESSED / "performance_clean.csv")
perf.columns = perf.columns.str.strip().str.lower()
perf = perf.rename(columns={"return_1yr_pct": "returns_1y", "return_3yr_pct": "returns_3y", "return_5yr_pct": "returns_5y", "expense_ratio_pct": "expense_ratio"})
perf = perf[[c for c in ["amfi_code","returns_1y","returns_3y","returns_5y","sharpe_ratio","expense_ratio","aum_crore"] if c in perf.columns]]
conn.execute("DROP TABLE IF EXISTS fact_performance")
perf.to_sql("fact_performance", conn, if_exists="replace", index=False)
print("✅ fact_performance:", len(perf))

# VALIDATION
print("\n📊 FINAL ROW COUNTS:")
for t in ["dim_fund","dim_date","fact_nav","fact_transactions","fact_performance"]:
    print(f"  {t}:", conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])

conn.commit()
conn.close()
print("\n🎯 DONE\n")