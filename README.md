# Medical Telegram Warehouse

## Overview
This project builds an end-to-end data pipeline that extracts medical-related Telegram channel data, stores it in PostgreSQL, and transforms it into analytics-ready tables using dbt.

The pipeline covers:
- Data ingestion from Telegram channels
- Raw storage in PostgreSQL
- Data modeling with dbt (staging → marts)
- Data validation via dbt tests
- Documentation via dbt docs

---

## Architecture

Telegram Channels  
→ Python Scraper (Telethon)  
→ Raw JSON Files  
→ PostgreSQL (raw schema)  
→ dbt Staging Layer  
→ dbt Mart Layer  
→ Analytical Models + Tests  

---

## Channels Scraped
- CheMed123  
- LobeliaCosmetics  
- tikvahpharma  

---

## Tech Stack
- Python (Telethon, psycopg2)
- PostgreSQL
- dbt (data build tool)
- SQL (analytics modeling)

---

## Project Structure

medical-telegram-warehouse/
│
├── data/ # Raw JSON + images
├── docs/ # Screenshots for dbt report
├── medical_warehouse/ # dbt project
│ ├── models/
│ │ ├── staging/
│ │ └── marts/
│ └── tests/
├── src/
│ ├── scraper.py
│ └── load_to_postgres.py
├── logs/
├── dbt_project.yml
└── README.md


---

## Pipeline Steps

### 1. Data Extraction
- Scrapes latest 200 messages per channel
- Downloads media (images)
- Stores structured JSON files

### 2. Data Loading
- Loads JSON into PostgreSQL table:
  `raw.telegram_messages`

### 3. dbt Transformations
- staging: `stg_telegram_messages`
- marts:
  - `dim_channels`
  - `dim_dates`
  - `fct_messages`

### 4. Data Quality Tests
- Ensure valid views
- Ensure no future timestamps
- Relationship constraints on facts

---

## How to Run

### 1. Scrape data
```bash
python src/scraper.py
2. Load into Postgres
python src/load_to_postgres.py
3. Run dbt
dbt run
dbt test
dbt docs generate
dbt docs serve
Outputs
Clean analytical tables in Postgres
dbt lineage graph
Tested and validated dataset
