
import pandas as pd
from pathlib import Path

# -----------------------------
# PATH SETUP
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "data" / "processed" / "transactions_clean.csv"

print("🔍 CHECKING TRANSACTIONS FILE COLUMNS")
print(f"File path: {file_path}")

# -----------------------------
# LOAD DATA
# -----------------------------
if not file_path.exists():
    raise FileNotFoundError(f"File not found: {file_path}")

df = pd.read_csv(file_path)

# -----------------------------
# SHOW COLUMN INFO
# -----------------------------
print("\n📊 COLUMNS FOUND:")
print(df.columns)

print("\n📌 FIRST 5 ROWS:")
print(df.head())