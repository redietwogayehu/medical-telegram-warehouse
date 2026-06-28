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
