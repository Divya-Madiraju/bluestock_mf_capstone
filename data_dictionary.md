# Data Dictionary — Bluestock MF Capstone

**Project:** Bluestock Mutual Fund Analytics  
**Database:** bluestock_mf.db (SQLite)  
**Last Updated:** June 2026

---

## Table of Contents
1. [dim_fund](#1-dim_fund)
2. [dim_date](#2-dim_date)
3. [fact_nav](#3-fact_nav)
4. [fact_transactions](#4-fact_transactions)
5. [fact_performance](#5-fact_performance)

---

## 1. dim_fund

**Source:** `data/raw/01_fund_master.csv`  
**Description:** Dimension table containing master information about each mutual fund scheme.

| Column | Data Type | Nullable | Business Definition |
|---|---|---|---|
| fund_id | INTEGER | NO | Auto-incremented primary key |
| amfi_code | INTEGER | NO | Unique AMFI scheme code assigned by AMFI India |
| fund_name | TEXT | YES | Full official name of the mutual fund scheme |
| fund_house | TEXT | YES | Asset Management Company (AMC) managing the fund |
| category | TEXT | YES | Broad category — Equity, Debt, Hybrid |
| sub_category | TEXT | YES | Sub-category — Large Cap, Small Cap, Liquid, etc. |
| risk_level | TEXT | YES | Risk grade — Low, Moderate, High, Very High |

---

## 2. dim_date

**Source:** Derived from `nav_clean.csv` and `transactions_clean.csv`  
**Description:** Date dimension table used for time-based analysis across all fact tables.

| Column | Data Type | Nullable | Business Definition |
|---|---|---|---|
| date_id | INTEGER | NO | Auto-incremented primary key |
| date | TEXT | NO | Date in YYYY-MM-DD format (unique) |
| year | INTEGER | YES | Calendar year extracted from date |
| month | INTEGER | YES | Calendar month (1–12) |
| day | INTEGER | YES | Day of month (1–31) |
| quarter | INTEGER | YES | Calendar quarter (1–4) |

---

## 3. fact_nav

**Source:** `data/processed/nav_clean.csv`  
**Original Raw File:** `data/raw/02_nav_history.csv`  
**Description:** Daily NAV (Net Asset Value) for each fund scheme. One row per fund per date.

| Column | Data Type | Nullable | Constraint | Business Definition |
|---|---|---|---|---|
| nav_id | INTEGER | NO | PK, Auto-increment | Surrogate primary key |
| amfi_code | INTEGER | NO | FK → dim_fund | AMFI scheme code identifying the fund |
| date | TEXT | NO | FK → dim_date | NAV date in YYYY-MM-DD format |
| nav | REAL | NO | nav > 0 | Net Asset Value in INR per unit on that date |

**Notes:**
- Missing NAV values for weekends/holidays are forward-filled (`ffill`)
- Duplicates removed during cleaning
- NAV must be greater than 0

---

## 4. fact_transactions

**Source:** `data/processed/transactions_clean.csv`  
**Original Raw File:** `data/raw/08_investor_transactions.csv`  
**Description:** Individual investor transactions. One row per transaction event.

| Column | Data Type | Nullable | Constraint | Business Definition |
|---|---|---|---|---|
| txn_id | INTEGER | NO | PK, Auto-increment | Surrogate primary key |
| amfi_code | INTEGER | NO | FK → dim_fund | Fund in which transaction was made |
| date | TEXT | NO | FK → dim_date | Transaction date in YYYY-MM-DD format |
| transaction_type | TEXT | YES | SIP / Lumpsum / Redemption | Type of investor transaction |
| amount | REAL | YES | amount > 0 | Transaction amount in INR |
| units | REAL | YES | Default 0 | Units purchased or redeemed |
| investor_state | TEXT | YES | — | Indian state of the investor |
| kyc_status | TEXT | YES | Verified / Pending / Rejected | KYC compliance status of the investor |

**Notes:**
- `transaction_type` standardised to SIP / Lumpsum / Redemption
- Amount validated to be greater than 0
- KYC status enum validated during cleaning

---

## 5. fact_performance

**Source:** `data/processed/performance_clean.csv`  
**Original Raw File:** `data/raw/07_scheme_performance.csv`  
**Description:** Performance metrics for each fund. One row per fund scheme.

| Column | Data Type | Nullable | Constraint | Business Definition |
|---|---|---|---|---|
| perf_id | INTEGER | NO | PK, Auto-increment | Surrogate primary key |
| amfi_code | INTEGER | NO | FK → dim_fund | AMFI scheme code identifying the fund |
| returns_1y | REAL | YES | — | Annualised return over 1 year (%) |
| returns_3y | REAL | YES | — | Annualised return over 3 years (%) |
| returns_5y | REAL | YES | — | Annualised return over 5 years (%) |
| sharpe_ratio | REAL | YES | — | Risk-adjusted return = (return − risk-free rate) / std dev |
| expense_ratio | REAL | YES | 0.1 – 2.5 | Annual fee charged by the fund as % of AUM |
| aum_crore | REAL | YES | — | Assets Under Management in INR Crore |

**Notes:**
- `expense_ratio` validated to be between 0.1% and 2.5%
- All return columns validated to be numeric
- Anomalies flagged during cleaning

---

## Source File Reference

| Raw File | Description |
|---|---|
| 01_fund_master.csv | Fund master with scheme metadata |
| 02_nav_history.csv | Daily NAV history for all schemes |
| 07_scheme_performance.csv | Fund performance and expense ratios |
| 08_investor_transactions.csv | Investor transaction records |

---

## Cleaning Rules Applied

| Rule | Applied To |
|---|---|
| Forward-fill missing NAV (ffill) | fact_nav |
| Remove duplicate rows | fact_nav, fact_transactions |
| Standardise transaction_type enum | fact_transactions |
| Validate amount > 0 | fact_transactions |
| Validate NAV > 0 | fact_nav |
| Validate expense_ratio 0.1–2.5% | fact_performance |
| Parse dates to YYYY-MM-DD | All tables |