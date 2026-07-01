from dagster import Definitions, asset, define_asset_job, ScheduleDefinition
import subprocess
import sys
import os
import json
from pathlib import Path

# -------------------------
# Project root
# -------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]

# -------------------------
# Environment
# -------------------------
ENV = os.environ.copy()
ENV["PYTHONUNBUFFERED"] = "1"


# -------------------------
# Helper: Run Python script
# -------------------------
def run_script(script_path: str):
    """
    Executes a Python script from the project root and exposes
    stdout/stderr if anything fails.
    """

    full_path = REPO_ROOT / script_path

    print(f"\n🚀 Running: {full_path}", flush=True)

    result = subprocess.run(
        [sys.executable, str(full_path)],
        cwd=REPO_ROOT,
        env=ENV,
        capture_output=True,
        text=True,
        timeout=600,
    )

    print("\n================ STDOUT ================\n", flush=True)
    print(result.stdout or "", flush=True)

    print("\n================ STDERR ================\n", flush=True)
    print(result.stderr or "", flush=True)

    print("\n================ RETURN CODE ================\n", flush=True)
    print(result.returncode, flush=True)

    if result.returncode != 0:
        raise Exception(
            "\n❌ SCRIPT FAILED\n"
            f"\nSCRIPT: {script_path}"
            f"\nRETURN CODE: {result.returncode}"
            f"\n\n--- STDERR ---\n{result.stderr or 'EMPTY'}"
            f"\n\n--- STDOUT ---\n{result.stdout or 'EMPTY'}"
        )

    return result.stdout


# -------------------------
# Asset 1: Telegram Scraper
# -------------------------
@asset
def telegram_raw_data():
    run_script("src/scraper.py")
    return "scraping_completed"


# -------------------------
# Asset 2: Load into PostgreSQL
# -------------------------
@asset
def cleaned_data(telegram_raw_data):
    run_script("src/load_to_postgres.py")
    return "load_completed"


# -------------------------
# Asset 3: YOLO Detection
# -------------------------
@asset
def yolo_detections(cleaned_data):
    run_script("src/detect_objects.py")

    output_path = REPO_ROOT / "data/processed/yolo_detections.json"

    if not output_path.exists():
        raise FileNotFoundError(
            f"YOLO output file not found:\n{output_path}"
        )

    with open(output_path, "r") as f:
        data = json.load(f)

    print(
        f"\n✅ Loaded {len(data)} image detection records from "
        f"{output_path}",
        flush=True,
    )

    return {
        "output_file": str(output_path),
        "images_processed": len(data),
    }


# -------------------------
# Job
# -------------------------
telegram_pipeline = define_asset_job(
    name="telegram_pipeline",
    selection="*",
)


# -------------------------
# Schedule
# -------------------------
daily_schedule = ScheduleDefinition(
    job=telegram_pipeline,
    cron_schedule="0 2 * * *",
)


# -------------------------
# Definitions
# -------------------------
defs = Definitions(
    assets=[
        telegram_raw_data,
        cleaned_data,
        yolo_detections,
    ],
    jobs=[
        telegram_pipeline,
    ],
    schedules=[
        daily_schedule,
    ],
)