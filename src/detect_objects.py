import json
from pathlib import Path

import psycopg2
from ultralytics import YOLO

# -----------------------------
# PostgreSQL configuration
# -----------------------------
DB_NAME = "postgres"
DB_USER = "betty"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "5432"

IMAGE_DIR = Path("data/raw/images")
OUTPUT_PATH = Path("data/processed/yolo_detections.json")

model = YOLO("yolov8n.pt")


# -----------------------------
# CATEGORY LOGIC
# -----------------------------
def categorize_objects(objects):
    objects = [o.lower() for o in objects]

    if any(o in ["laptop", "cell phone", "keyboard", "mouse", "tv"] for o in objects):
        return "electronics"

    if any(o in ["bottle", "pill", "medicine", "cup"] for o in objects):
        return "medical_product"

    if "person" in objects:
        return "people"

    # REQUIRED 4th category explicitly defined
    if any(o in ["book", "stop sign", "refrigerator", "bird", "dining table"] for o in objects):
        return "general_objects"

    return "other"


# -----------------------------
# PostgreSQL connection
# -----------------------------
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
)

cur = conn.cursor()

print("Running YOLO inference...")

all_results = []

# -----------------------------
# PROCESS IMAGES
# -----------------------------
for image_file in IMAGE_DIR.glob("*"):

    if image_file.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
        continue

    print(f"Processing {image_file.name}")

    results = model(str(image_file))

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

    detected_objects = []
    detections = []

    # -----------------------------
    # Parse detections
    # -----------------------------
    for result in results:
        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            label = model.names[class_id]

            detected_objects.append(label)

            detections.append(
                {
                    "object": label,
                    "confidence": round(confidence, 4),
                }
            )

    image_category = categorize_objects(detected_objects)

    # -----------------------------
    # Save for JSON artifact
    # -----------------------------
    all_results.append(
        {
            "image": image_file.name,
            "image_path": str(image_file),
            "message_id": message_id,
            "channel_name": channel_name,
            "category": image_category,
            "detections": detections,
        }
    )

    # -----------------------------
    # Insert into PostgreSQL
    # -----------------------------
    for detection in detections:

        cur.execute(
            """
            INSERT INTO raw.fct_image_detections
            (
                message_id,
                channel_name,
                image_path,
                detected_object,
                confidence,
                image_category
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                message_id,
                channel_name,
                str(image_file),
                detection["object"],
                detection["confidence"],
                image_category,
            ),
        )

# -----------------------------
# Commit DB changes
# -----------------------------
conn.commit()

cur.close()
conn.close()

# -----------------------------
# Save JSON artifact for Dagster
# -----------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_PATH, "w") as f:
    json.dump(all_results, f, indent=2)

print(f"[SAVED] YOLO results → {OUTPUT_PATH}")
print(f"[INFO] Images processed: {len(all_results)}")
print("Detection pipeline completed.")