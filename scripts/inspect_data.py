import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

files = [
    "nav_clean.csv",
    "transactions_clean.csv",
    "performance_clean.csv"
]

print("\n🔍 DATA INSPECTION STARTED\n")

for file in files:
    path = DATA_DIR / file

    if not path.exists():
        print(f"❌ Missing file: {file}")
        continue

    df = pd.read_csv(path)

    print(f"\n📊 FILE: {file}")
    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print(df.head(2))