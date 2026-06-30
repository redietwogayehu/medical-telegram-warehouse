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