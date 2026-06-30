from dagster import Definitions
from pipelines.assets import run_scraper, load_to_postgres, run_dbt

defs = Definitions(
    assets=[run_scraper, load_to_postgres, run_dbt]
)