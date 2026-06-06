
print("🔥 SCRIPT IS RUNNING")

from pathlib import Path
import pandas as pd

# -----------------------------
# PATH SETUP
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
RAW = BASE_DIR / "data" / "raw"
PROCESSED = BASE_DIR / "data" / "processed"

PROCESSED.mkdir(parents=True, exist_ok=True)

# -----------------------------
# LOAD FUNCTION
# -----------------------------
def load_data(filename):
    file_path = RAW / filename
    print(f"Loading file: {file_path}")

    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")

    return pd.read_csv(file_path)

# -----------------------------
# SAVE FUNCTION
# -----------------------------
def save_data(df, filename):
    output_path = PROCESSED / filename
    df.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")

# -----------------------------
# CLEAN NAV
# -----------------------------
def clean_nav(df):
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date', 'nav'])
    df = df.sort_values(['amfi_code', 'date'])
    df = df.drop_duplicates()
    df = df[df['nav'] > 0]
    df['nav'] = df.groupby('amfi_code')['nav'].ffill()
    return df

# -----------------------------
# CLEAN TRANSACTIONS
# -----------------------------
def clean_transactions(df):
    date_col = [c for c in df.columns if "date" in c.lower()]
    if date_col:
        df[date_col[0]] = pd.to_datetime(df[date_col[0]], errors='coerce')

    type_col = [c for c in df.columns if "type" in c.lower()]
    if type_col:
        df[type_col[0]] = df[type_col[0]].astype(str).str.upper()

    if 'amount' in df.columns:
        df = df[df['amount'] > 0]

    df = df.dropna()
    return df

# -----------------------------
# CLEAN PERFORMANCE
# -----------------------------
def clean_performance(df):
    for col in df.columns:
        df[col] = df[col].astype(str)
        df[col] = df[col].str.replace('%', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(how='all')

    if 'expense_ratio' in df.columns:
        df = df[
            (df['expense_ratio'] >= 0.1) &
            (df['expense_ratio'] <= 2.5)
        ]

    return df

# -----------------------------
# MAIN
# -----------------------------
def main():
    print("\n🚀 MAIN STARTED\n")

    nav = load_data("02_nav_history.csv")
    print("NAV shape:", nav.shape)
    nav = clean_nav(nav)
    save_data(nav, "nav_clean.csv")

    txn = load_data("08_investor_transactions.csv")
    print("Transactions shape:", txn.shape)
    txn = clean_transactions(txn)
    save_data(txn, "transactions_clean.csv")

    perf = load_data("07_scheme_performance.csv")
    print("Performance shape:", perf.shape)
    perf = clean_performance(perf)
    save_data(perf, "performance_clean.csv")

    print("\n🎯 ETL COMPLETED SUCCESSFULLY\n")

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    main()