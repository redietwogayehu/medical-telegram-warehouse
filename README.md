# Medical Telegram Warehouse

## Overview

This project implements an end-to-end data engineering pipeline that collects medical-related Telegram data, transforms it into an analytical warehouse, enriches image data using YOLOv8 object detection, exposes analytics through a FastAPI service, and orchestrates the workflow with Dagster.

The project was developed for **Kara Solutions** to enable analytical insights from Ethiopian medical Telegram channels.

---

## Business Objective

The goal is to build a robust ELT pipeline capable of transforming raw Telegram data into a structured analytical warehouse for answering business questions such as:

- Which medical products are mentioned most frequently?
- Which Telegram channels are the most active?
- How does engagement (views and forwards) change over time?
- What visual objects appear most often in medical advertisements?
- Which channels generate the highest audience engagement?

---

# Architecture

```
Telegram Channels
        │
        ▼
 Python Scraper (Telethon)
        │
        ▼
 Raw JSON + Images (Data Lake)
        │
        ▼
 PostgreSQL Data Warehouse
        │
        ▼
 dbt Transformations
(Staging → Star Schema)
        │
        ▼
 YOLOv8 Image Detection
        │
        ▼
 FastAPI Analytical Endpoints
        │
        ▼
 Dagster Pipeline Orchestration
```

---

## Channels Scraped

- CheMed123
- LobeliaCosmetics
- tikvahpharma

---

# Technology Stack

- Python
- Telethon
- PostgreSQL
- dbt
- SQL
- YOLOv8 (Ultralytics)
- FastAPI
- Dagster
- psycopg2

---

# Project Structure

```
medical-telegram-warehouse/

├── api/
│   ├── main.py
│   ├── routes.py
│   └── database.py
│
├── data/
│   ├── raw/
│   │   ├── telegram_messages/
│   │   └── images/
│
├── docs/
│   └── screenshots/
│
├── medical_warehouse/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── tests/
│
├── pipelines/
│   ├── definitions.py
│   └── dagster/
│
├── src/
│   ├── scraper.py
│   ├── load_to_postgres.py
│   └── detect_objects.py
│
├── requirements.txt
├── dbt_project.yml
└── README.md
```

---

# Pipeline Workflow

## Task 1 — Telegram Data Collection

- Scrape Telegram messages using Telethon
- Download message images
- Store raw JSON files
- Build the project data lake

---

## Task 2 — Data Warehouse & dbt

Load raw data into PostgreSQL.

Create a dimensional warehouse consisting of:

- `stg_telegram_messages`
- `dim_channels`
- `dim_dates`
- `fct_messages`

Run dbt tests to validate:

- Non-null values
- Relationships
- Positive view counts
- No future timestamps

Generate dbt documentation and lineage graphs.

---

## Task 3 — Image Enrichment

YOLOv8 is used to detect objects within downloaded Telegram images.

Detected objects are stored in:

- `fct_image_detections`

Example attributes include:

- message_id
- channel_name
- detected_object
- confidence
- image_path

---

## Task 4 — Analytical API

FastAPI exposes analytical endpoints including:

- Top products
- Channel activity
- Message search
- Image detection statistics

Run locally:

```bash
uvicorn api.main:app --reload
```

Interactive documentation:

```
http://127.0.0.1:8000/docs
```

---

## Task 5 — Pipeline Orchestration

Dagster orchestrates the pipeline through software-defined assets.

Current assets include:

- telegram_raw_data
- cleaned_data
- yolo_detections

Launch Dagster:

```bash
dagster dev -f pipelines/definitions.py
```

---

# Running the Project

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Scrape Telegram

```bash
python src/scraper.py
```

## 3. Load PostgreSQL

```bash
python src/load_to_postgres.py
```

## 4. Run dbt

```bash
dbt run
dbt test
dbt docs generate
dbt docs serve
```

## 5. Run YOLO Detection

```bash
python src/detect_objects.py
```

## 6. Start FastAPI

```bash
uvicorn api.main:app --reload
```

## 7. Start Dagster

```bash
dagster dev -f pipelines/definitions.py
```

---

# Outputs

The project produces:

- Raw Telegram JSON data
- Downloaded Telegram images
- PostgreSQL analytical warehouse
- dbt star schema
- dbt documentation and lineage graph
- YOLOv8 object detections
- FastAPI analytical endpoints
- Dagster orchestration pipeline

---

# Screenshots

The repository includes screenshots demonstrating:

- dbt execution
- dbt documentation
- dbt lineage graph
- FastAPI Swagger UI
- Dagster UI
- Pipeline execution

---

# Future Improvements

- Incremental dbt models
- Scheduled pipeline execution
- Entity recognition for medicines
- Sentiment analysis
- Advanced product recommendation analytics
- Production deployment using Docker and cloud infrastructure
