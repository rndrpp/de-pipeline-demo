# de-pipeline-demo

A local ELT pipeline built with Docker, Apache Airflow, dbt, and BigQuery.

## Architecture
## Stack
- **Airflow** — orchestrates the pipeline, runs daily
- **BigQuery** — cloud data warehouse
- **dbt** — transforms raw data into clean, deduplicated models
- **Docker** — runs Airflow locally without installing anything

## Models
- `stg_exchange_rates` — cleans and casts raw exchange rate data
- `mart_latest_rates` — deduplicates to 1 row per day (latest fetch wins)

## How to Run

### 1. Start Airflow
```bash
docker compose up airflow-webserver airflow-scheduler -d
```

### 2. Open Airflow UI
Go to `http://localhost:8080` and trigger `exchange_rate_pipeline`

### 3. Run dbt
```bash
docker run --rm \
  -v ~/de-pipeline-demo/dbt/exchange_rates:/usr/app \
  -v ~/de-pipeline-demo/gcp-key.json:/gcp-key.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/gcp-key.json \
  --entrypoint /bin/bash \
  ghcr.io/dbt-labs/dbt-bigquery:1.7.7 \
  -c "cd /usr/app && dbt run --profiles-dir profiles"
```

## Notes
- `gcp-key.json` is excluded from Git — add your own service account key
- Dataset location: `asia-southeast2` (Jakarta)
