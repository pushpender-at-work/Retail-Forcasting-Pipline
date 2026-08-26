📈 Retail Demand Forecasting Pipeline

End-to-end ML system that predicts store-level sales 30 days out, flags stockout risk, and retrains itself automatically — built to mirror how retail chains run real forecasting infrastructure.

🎯 Problem

Retail chains lose money two ways: overstocking (dead capital, markdowns) and understocking (lost sales, unhappy customers). Manual forecasting doesn't scale across 1,000+ stores.

This pipeline forecasts demand per store, automatically flags stockout risk, and retrains weekly without human intervention — the same pattern used in production inventory systems.


⚙️ How It Works
Raw Sales Data (MySQL)
        │
        ▼
   ETL Pipeline (Python)
        │
        ▼
  Prophet Forecasting (1,115 models — one per store)
        │
        ▼
  Predictions Store (MySQL, star schema)
        │
        ├──► Streamlit Dashboard (interactive forecasts + alerts)
        │
        └──► GitHub Actions (weekly auto-retrain)
Ingest — Historical sales data (1,115 stores, 2 years) loaded into a MySQL star schema
Forecast — Prophet trains an independent time-series model per store, generating 30-day sales predictions
Alert — Predicted demand is compared against current stock thresholds to flag stores at risk of running out
Serve — Streamlit dashboard lets users explore forecasts, filter by store, and view stockout alerts
Automate — GitHub Actions retrains all models weekly on a schedule, with error handling and logging
🧱 Tech Stack
Layer	Technology
Data storage	MySQL (star schema)
ETL	Python (pandas)
Forecasting	Prophet
Dashboard	Streamlit
Automation / CI-CD	GitHub Actions
Deployment	Streamlit Cloud
📊 By the Numbers
1,115 independent store-level ML models
33,000+ individual sales predictions generated
2 years of historical data per store
Weekly automated retraining — zero manual intervention
Star schema database design for fast analytical queries
🗂️ Dataset

Rossmann Store Sales — 1,115 stores, ~2 years of daily sales history, including promotions, holidays, and store metadata.

-- Key Features
Per-store forecasting — not one generic model, but 1,115 individually trained models capturing store-specific seasonality
Stockout risk alerts — automatically flags stores where forecasted demand exceeds available stock
Self-retraining — GitHub Actions triggers weekly retraining, keeping forecasts current without manual runs
Interactive exploration — filter by store, date range, and view forecast confidence intervals
Production patterns — structured ETL, error handling, and automated pipelines rather than a one-off notebook
-- Architecture Decisions

Why Prophet? Handles seasonality, holidays, and missing data out of the box — well suited to retail sales patterns with minimal tuning overhead compared to deep learning approaches for this scale of data.

Why per-store models instead of one global model? Each store has distinct seasonality, local demand patterns, and promotional effects. Individual models outperform a single pooled model on store-level accuracy.

Why a star schema? Keeps forecast queries fast as the dataset grows, and separates fact data (sales, predictions) from dimension data (store metadata) — the same design pattern used in real retail data warehouses.

Why GitHub Actions for retraining? Demonstrates CI/CD thinking applied to ML — models decay as new data arrives, so retraining needs to be scheduled and automated, not manual.

-- Run It Locally
bash
# Clone the repo
git clone <your-repo-url>
cd retail-demand-forecasting

# Install dependencies
pip install -r requirements.txt

# Set up MySQL database
mysql -u root -p < schema/setup.sql

# Run ETL + training
python pipeline/run_pipeline.py

# Launch dashboard
streamlit run app.py
📁 Project Structure
retail-demand-forecasting/
├── .github/workflows/
│   └── retrain.yml          # Weekly automated retraining
├── etl/
│   └── load_data.py         # Data ingestion + cleaning
├── models/
│   └── train_forecast.py    # Prophet training per store
├── schema/
│   └── setup.sql            # MySQL star schema
├── app.py                   # Streamlit dashboard
├── requirements.txt
└── README.md
-> Future Improvements
Add external regressors (weather, local events) to Prophet models
Replace per-store retraining loop with parallelized batch processing
Add model performance monitoring (MAPE tracking over time)
Extend stockout alerts to trigger automated reorder recommendations
