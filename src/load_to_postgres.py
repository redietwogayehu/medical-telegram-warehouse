import os
import json
import psycopg2
from datetime import datetime

# ----------------------------
# DATABASE CONFIG (FIXED)
# ----------------------------
DB_CONFIG = {
    "dbname": "medical_warehouse",
    "user": "betty",          # FIXED (your real Postgres role)
    "password": "",           # Mac/Homebrew usually empty unless you set it
    "host": "localhost",
    "port": 5432
}

# ----------------------------
# RAW DATA PATH
# ----------------------------
RAW_DIR = "data/raw/telegram_messages/2026-06-28"

# ----------------------------
# CONNECT TO POSTGRES
# ----------------------------
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

print("[INFO] Connected to PostgreSQL")

# ----------------------------
# LOAD FILES
# ----------------------------
for file in os.listdir(RAW_DIR):
    if file.endswith(".json"):
        channel = file.replace(".json", "")
        path = os.path.join(RAW_DIR, file)

        print(f"[INFO] Loading file: {file}")

        with open(path, "r") as f:
            data = json.load(f)
    # ----------------------------
# SKIP EMPTY FILES (ADD THIS)
# ----------------------------
        if len(data) == 0:
            print(f"[SKIP] {file} is empty")
        continue
        inserted = 0

        for row in data:
            try:
                cur.execute("""
                    INSERT INTO raw.telegram_messages (
                        message_id,
                        channel_name,
                        message_date,
                        message_text,
                        has_media,
                        image_path,
                        views,
                        forwards
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    row["message_id"],
                    row["channel_name"],
                    row["message_date"],
                    row["message_text"],
                    row["has_media"],
                    row["image_path"],
                    row["views"],
                    row["forwards"]
                ))

                inserted += 1

            except Exception as e:
                print(f"[ERROR] Row insert failed: {e}")
                conn.rollback()

        conn.commit()
        print(f"[DONE] Inserted {inserted} rows from {file}")

# ----------------------------
# CLEANUP
# ----------------------------
cur.close()
conn.close()

print("DONE: Data loaded into PostgreSQL")