import os
from pathlib import Path

import psycopg2
from ultralytics import YOLO

# -----------------------------
# PostgreSQL configuration
# -----------------------------
DB_NAME = "postgres"
DB_USER = "betty"
DB_PASSWORD = ""      # Leave blank if you don't use a password
DB_HOST = "localhost"
DB_PORT = "5432"

IMAGE_DIR = Path("data/raw/images")

# Load YOLO model
model = YOLO("yolov8n.pt")

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
)

cur = conn.cursor()

print("Running YOLO inference...")

for image_file in IMAGE_DIR.glob("*"):

    if image_file.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
        continue

    print(f"Processing {image_file.name}")

    results = model(str(image_file))

    # Determine channel and message id from filename
    filename = image_file.stem

    if "_" in filename:
        channel_name = filename.rsplit("_", 1)[0]

        try:
            message_id = int(filename.rsplit("_", 1)[1])
        except ValueError:
            message_id = None
    else:
        channel_name = "Unknown"
        message_id = None

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            detected_object = model.names[class_id]

            cur.execute(
                """
                INSERT INTO raw.fct_image_detections
                (
                    message_id,
                    channel_name,
                    image_path,
                    detected_object,
                    confidence
                )
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    message_id,
                    channel_name,
                    str(image_file),
                    detected_object,
                    confidence,
                ),
            )

conn.commit()

cur.close()
conn.close()

print("Detection pipeline completed.")