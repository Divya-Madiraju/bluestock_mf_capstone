import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

db_path = BASE_DIR / "data" / "db" / "bluestock_mf.db"
sql_path = BASE_DIR / "sql" / "schema.sql"

# Create folders if not exist
db_path.parent.mkdir(parents=True, exist_ok=True)

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Read schema.sql
with open(sql_path, "r", encoding="utf-8") as f:
    schema = f.read()

# Execute schema
cursor.executescript(schema)

conn.commit()
conn.close()

print(" Database created and schema executed successfully")