import sqlite3
from pathlib import Path

BASE_DIR = Path.cwd()
db_path = BASE_DIR / "data" / "db" / "bluestock_mf.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("TABLES CREATED:")
for t in tables:
    print(t[0])

conn.close()