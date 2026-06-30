from dagster import Definitions, asset, define_asset_job

@asset
def telegram_raw_data():
    return [
        {"message_id": 1, "text": "sample medical post", "views": 100},
    ]

@asset
def cleaned_data(telegram_raw_data):
    return telegram_raw_data

@asset
def yolo_detections(cleaned_data):
    return cleaned_data

telegram_pipeline = define_asset_job(
    name="telegram_pipeline",
    selection="*",
)

defs = Definitions(
    assets=[telegram_raw_data, cleaned_data, yolo_detections],
    jobs=[telegram_pipeline],
)