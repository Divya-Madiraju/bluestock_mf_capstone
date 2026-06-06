import sqlite3
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH      = BASE_DIR / "data" / "db" / "bluestock_mf.db"
QUERIES_PATH = BASE_DIR / "sql" / "queries.sql"

conn = sqlite3.connect(DB_PATH)

with open(QUERIES_PATH, "r", encoding="utf-8") as f:
    sql = f.read()

# Match "-- Q1: label\nSELECT...;" blocks
pattern = re.compile(r"-- (Q\d+:[^\n]+)\n(.*?)(?=\n-- Q\d+:|\Z)", re.DOTALL)
matches = pattern.findall(sql)

if not matches:
    print("⚠️  No queries found. Check queries.sql format.")
else:
    for label, query in matches:
        query = query.strip().rstrip(";")
        if not query:
            continue
        try:
            cursor = conn.execute(query)
            rows = cursor.fetchall()
            cols = [d[0] for d in cursor.description] if cursor.description else []
            print(f"\n{'='*55}")
            print(f"📊 {label.strip()}")
            print(f"{'='*55}")
            print("  " + " | ".join(cols))
            print("  " + "-" * 50)
            for row in rows[:5]:
                print(" ", row)
            if not rows:
                print("  (no rows returned)")
        except Exception as e:
            print(f"❌ Error in {label.strip()}: {e}")

conn.close()
print("\n✅ Done.")