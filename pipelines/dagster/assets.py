from dagster import asset
import os
import subprocess

@asset
def run_scraper():
    subprocess.run(["python", "src/scraper.py"], check=True)
    return "scraped"


@asset
def load_to_postgres(run_scraper):
    subprocess.run(["python", "src/load_to_postgres.py"], check=True)
    return "loaded"


@asset
def run_dbt(load_to_postgres):
    os.chdir("medical_warehouse")
    subprocess.run(["dbt", "run"], check=True)
    return "dbt complete"

from dagster import asset
import subprocess


@asset(
    description="Runs YOLOv8 inference and stores image detections into PostgreSQL"
)
def yolo_detections():
    result = subprocess.run(
        ["python", "src/detect_objects.py"],
        capture_output=True,
        text=True,
        check=True
    )

    print(result.stdout)
    return "YOLO inference completed"