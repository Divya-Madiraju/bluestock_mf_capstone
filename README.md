# Bluestock MF Capstone Project

## Overview
Mutual Fund analytics platform built on AMFI data covering 40 schemes (2022–2026).

## Project Structure
- `data/` — raw, processed CSVs and SQLite DB
- `notebooks/` — Jupyter notebooks for EDA and analytics
- `scripts/` — ETL pipeline and utility scripts
- `sql/` — Schema and analytical queries
- `dashboard/` — Power BI dashboard
- `reports/` — Final report and presentation

## How to Run
1. `python scripts/etl_pipeline.py`
2. `python scripts/load_to_sqlite.py`
3. Open notebooks in order 01 → 05

## Tech Stack
Python, Pandas, SQLite, Power BI, Plotly, Seaborn