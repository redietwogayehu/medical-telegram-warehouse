# Medical Telegram Warehouse

## Overview

Medical Telegram Warehouse is an end-to-end ELT data engineering project developed for **Kara Solutions**. The pipeline collects medical-related content from Ethiopian Telegram channels, stores raw data in PostgreSQL, transforms it into an analytical warehouse using dbt, enriches images with YOLOv8 object detection, exposes analytical insights through FastAPI, and orchestrates workflows using Dagster.

The project demonstrates a complete modern data engineering workflow from data ingestion to analytics-ready datasets and APIs.

---

# Business Objective

The objective is to build a scalable analytical platform that converts unstructured Telegram data into structured business intelligence.

The platform enables analysis such as:

- Identifying the most frequently promoted medical products
- Comparing activity across Telegram channels
- Measuring engagement using views and forwards
- Tracking posting trends over time
- Detecting visual objects appearing in advertisements using YOLOv8

---

# Architecture

```text
Telegram Channels
        │
        ▼
Python Scraper (Telethon)
        │
        ▼
Raw JSON + Images (Data Lake)
        │
        ▼
PostgreSQL (Raw Layer)
        │
        ▼
dbt Transformations
(Staging → Star Schema)
        │
        ▼
YOLOv8 Image Detection
        │
        ▼
FastAPI Analytics API
        │
        ▼
Dagster Pipeline Orchestration
```

---

# Telegram Channels

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

# Repository Structure

```text
medical-telegram-warehouse/

├── api/
│   ├── main.py
│   ├── routes.py
│   └── database.py
│
├── data/
│   └── raw/
│       ├── telegram_messages/
│       └── images/
│
├── docs/
│   └── screenshots/
│       ├── api/
│       ├── dagster/
│       ├── dbt/
│       └── yolo/
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

# Project Workflow

## Task 1 — Telegram Data Collection

The pipeline uses **Telethon** to:

- Extract Telegram messages
- Download associated images
- Save raw JSON files
- Build the project's data lake

---

## Task 2 — Data Warehouse & dbt

Raw Telegram data is loaded into PostgreSQL under the **raw** schema.

dbt transforms the data into an analytical star schema consisting of:

### Staging

- `stg_telegram_messages`

### Dimensions

- `dim_channels`
- `dim_dates`

### Fact Tables

- `fct_messages`

Data quality tests validate:

- Non-null fields
- Valid relationships
- Positive engagement metrics
- Valid timestamps

dbt also generates documentation and lineage graphs.

---

## Task 3 — YOLOv8 Image Enrichment

Downloaded Telegram images are processed using **YOLOv8** object detection.

Detected objects are stored in PostgreSQL:

```
raw.fct_image_detections
```

Each record contains:

- message_id
- channel_name
- image_path
- detected_object
- confidence
- created_at

This enrichment enables future visual analytics alongside message metadata.

---

## Task 4 — Analytical API

FastAPI exposes analytical endpoints for querying warehouse data.

Example endpoints include:

- `/top-products`
- `/channel-activity`
- `/messages/search`
- `/image-detections`

Run locally:

```bash
uvicorn api.main:app --reload
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

## Task 5 — Pipeline Orchestration

Dagster orchestrates the pipeline using software-defined assets.

Current assets include:

- telegram_raw_data
- cleaned_data
- yolo_detections

Launch Dagster:

```bash
dagster dev -f pipelines/definitions.py
```

---

# Getting Started

## Clone the repository

```bash
git clone https://github.com/redietwogayehu/medical-telegram-warehouse.git
cd medical-telegram-warehouse
```

## Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Pipeline

### 1. Scrape Telegram data

```bash
python src/scraper.py
```

### 2. Load data into PostgreSQL

```bash
python src/load_to_postgres.py
```

### 3. Build the warehouse

```bash
dbt run
dbt test
dbt docs generate
dbt docs serve
```

### 4. Perform YOLOv8 image detection

```bash
python src/detect_objects.py
```

### 5. Launch the API

```bash
uvicorn api.main:app --reload
```

### 6. Launch Dagster

```bash
dagster dev -f pipelines/definitions.py
```

---

# Project Outputs

The completed pipeline produces:

- Raw Telegram JSON files
- Downloaded Telegram images
- PostgreSQL warehouse tables
- dbt staging and mart models
- Star schema for analytics
- dbt documentation and lineage
- YOLOv8 image detections stored in PostgreSQL
- FastAPI analytical endpoints
- Dagster orchestration workflow

---

# Screenshots

The repository includes screenshots demonstrating:

- Telegram scraping
- dbt execution
- dbt documentation
- dbt lineage graph
- YOLOv8 inference
- PostgreSQL image detections
- FastAPI Swagger UI
- Dagster UI and asset execution

---

# Future Improvements

- Incremental dbt models
- Scheduled Dagster jobs
- Medical entity recognition
- Sentiment analysis
- Product recommendation analytics
- Docker containerization
- Cloud deployment
