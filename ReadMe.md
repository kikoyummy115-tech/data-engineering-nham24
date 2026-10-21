# 🛵 Nham24 Customer & Logistics Data Pipeline

An end-to-end Data Engineering pipeline designed to extract, transform, validate, and load localized on-demand super-app data (food delivery, mart, and express courier) for **Nham24 Cambodia**.

This project processes raw, nested JSON payloads into an analytics-ready dimensional schema in PostgreSQL, orchestrates workflow execution with Apache Airflow, validates data quality using Soda Core, and serves interactive executive insights via Streamlit.

---

## 🏗️ Architecture Overview

```text
  [ Operational Source ]
         │  (Mock API / JSON Payloads)
         ▼
  ┌────────────────────────────────────────────────────────┐
  │ 1. EXTRACT (Python / Requests)                         │
  │    Pulls raw nested JSON into data/raw/                │
  └────────────────────────┬───────────────────────────────┘
                           │
                           ▼
  ┌────────────────────────────────────────────────────────┐
  │ 2. TRANSFORM (Python / Functional ETL)                 │
  │    Normalizes 1:N relations (Addresses & Payments)     │
  │    Cleans timestamps, currencies (USD/KHR), and coords │
  └────────────────────────┬───────────────────────────────┘
                           │
                           ▼
  ┌────────────────────────────────────────────────────────┐
  │ 3. LOAD (psycopg3 / PostgreSQL)                        │
  │    Upserts into normalized target tables               │
  │    (customers, customer_addresses, payment_methods)   │
  └────────────────────────┬───────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
  ┌──────────────────────┐    ┌───────────────────────────┐
  │ 4. DATA QUALITY      │    │ 5. BUSINESS ANALYTICS     │
  │    Soda Core checks  │    │    Streamlit Dashboard    │
  │    (Bounds, formats) │    │    Interactive BI metrics │
  └──────────────────────┘    └───────────────────────────┘
```

---

## 🚀 Key Features

- **Domain-Specific Transformations:** Handles Cambodian administrative subdivisions (Khan and Sangkat), dual-currency setups (`USD` and `KHR`), and local payment gateways (`Bakong KHQR`, `ABA PayWay`, `Wing`, `Cash on Delivery`).
- **Normalized Relational Model:** Deconstructs complex document structures into 3 relational entities with strict primary/foreign key integrity.
- **Idempotent Loading:** Uses `ON CONFLICT (...) DO UPDATE` upsert logic to ensure safe pipeline re-runs without data duplication.
- **Data Quality as Code:** Automated assertions via Soda Core enforcing geographic bounds (Cambodia lat/long), regex email validation, and non-empty checks.
- **Workflow Orchestration:** Airflow DAG configuration leveraging the TaskFlow API for parallel table loads.
- **Business Intelligence:** Interactive Streamlit dashboard with KPI cards and district logistics heatmaps.

---

## 📁 Repository Structure

```text
├── dags/
│   └── data_pipeline.py       # Apache Airflow DAG definition
├── data/
│   └── raw/                   # Bronze layer landing directory
├── soda/
│   ├── checks.yml             # Soda Core data validation contracts
│   └── configuration.yml      # Data source connection definitions
├── sql/
│   └── schema.sql             # DDL for customers, addresses, and payments
├── src/
│   ├── extract.py             # API extraction logic
│   ├── transform.py           # Pure transformation functions
│   ├── load.py                # Database ingestion & upserts via psycopg
│   └── pipeline.py            # Local pipeline runner
├── tests/
│   └── test_transform.py      # Unit tests for transformation functions
├── .env.example               # Environment variable templates
├── dashboard.py               # Streamlit business analytics dashboard
├── requirements.txt           # Project dependencies
└── README.md
```

---

## 📊 Data Schema (`sql/schema.sql`)

### 1. `customers`
Stores user identity, communication preferences, loyalty tiers, and audit metadata.
- `customer_id` (PK), `full_name`, `phone_number`, `email`, `preferred_language`, `preferred_currency`, `loyalty_tier`, `points_balance`, `lifetime_orders_count`, `processed_at`.

### 2. `customer_addresses`
Stores delivery pins, building instructions, and administrative boundaries.
- `address_id` (PK), `customer_id` (FK), `label`, `is_default`, `latitude`, `longitude`, `street`, `sangkat`, `khan`, `city`, `dropoff_notes`, `processed_at`.

### 3. `customer_payment_methods`
Tracks tokenized bank accounts, card rails, and cash preferences.
- `payment_method_id` (PK), `customer_id` (FK), `payment_type`, `bank_name`, `account_mask`, `is_default`, `processed_at`.

---

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.10+
- PostgreSQL 14+ (or Docker)
- Git

### 2. Clone and Setup Environment
```bash
git clone https://github.com/kikoyummy115-tech/data-engineering-nham24.git
cd data-engineering-nham24

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/datawarehouse
```

### 4. Run Migrations & Ingestion Pipeline
```bash
# Run end-to-end extraction, transformation, and ingestion
python src/pipeline.py
```

### 5. Run Unit Tests
```bash
python -m unittest discover tests/
```

### 6. Run Data Quality Checks (Soda Core)
```bash
soda scan -d nham24_warehouse -c soda/configuration.yml soda/checks.yml
```

### 7. Launch the Analytics Dashboard
```bash
streamlit run dashboard.py
```
Open your browser at `http://localhost:8501` to view delivery densities, payment methods adoption, and loyalty tier insights.

---

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.