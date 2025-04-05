# Spotify Data Pipeline

![image](https://github.com/user-attachments/assets/c5f8449a-29ad-4266-9942-5363276fde0a)

An end-to-end data engineering pipeline designed to extract music streaming data from the Spotify API, store it in a PostgreSQL database, perform advanced transformations using dbt, orchestrate the workflow with Apache Airflow, and visualize insights using Metabase.

This project serves as a reference implementation for best practices in modern Data Engineering using open-source tools and cloud-native workflows.

## Objective

Build a robust and reproducible ETL pipeline capable of:

- Extracting recently played tracks from a user's Spotify account.
- Storing raw and processed data into a PostgreSQL database.
- Transforming the data using dbt (data build tool).
- Orchestrating the ETL steps using Apache Airflow.
- Visualizing insights and KPIs via Metabase dashboards.

This pipeline was built to demonstrate the complete data lifecycle using Spotify data as a source, while emphasizing modularity, maintainability, observability, and documentation.

## Tools & Technologies Used

| Stage          | Tool / Technology      | Purpose                                 |
| -------------- | ---------------------- | --------------------------------------- |
| Ingestion      | Python, Spotipy        | Extract data from Spotify API           |
| Transformation | dbt (data build tool)  | Data modeling & transformation (SQL)    |
| Orchestration  | Apache Airflow         | Workflow scheduling & dependency mgmt   |
| Infrastructure | Docker, Docker Compose | Containerization & deployment           |
| Storage        | PostgreSQL             | Raw & transformed data storage          |
| Visualization  | Metabase               | Dashboards & visual analytics           |
| Testing        | Pytest, dbt tests      | Data ingestion, schema & model tests    |
| Configuration  | dotenv (.env)          | Secrets management                      |

## Pipeline Architecture

### Ingestion

- The Spotify API is accessed using a Python script (`save_recent_tracks.py`) via the Spotipy library.
- Data is collected and written to a PostgreSQL table named recent_tracks.
- The ingestion script is triggered daily by an Airflow DAG.

### Transformation

- dbt models perform SQL-based transformations:
   - `stg_recent_tracks`: cleans and standardizes raw data.
   - `top_artists`: calculates top artists and average listening time.
   - `top_albums`: aggregates album play statistics.
   - `track_duration_buckets`: classifies tracks by length.
   - `listening_by_hour`: aggregates play counts by time of day.

### Orchestration

- Apache Airflow schedules and orchestrates the pipeline execution.
- The DAG includes retry logic, task dependencies, and descriptive tags.

### Visualization

- Metabase connects directly to PostgreSQL.
- Dynamic dashboards show track play history, artist trends, and listening behavior.

## Airflow DAG Flow

![image](https://github.com/user-attachments/assets/57ba9ace-26d8-43f2-a498-f567002698d8)

### DAG Process Overview

- The DAG, defined in `spotify_pipeline_dag.py`, manages the pipeline in three key tasks:
   - `extract_recent_tracks`: Authenticates with the Spotify API and extracts the last 50 played tracks into PostgreSQL.
   - `run_dbt_models`: Executes SQL-based transformation models using dbt run.
   - `run_dbt_tests`: Validates the resulting models using dbt test to ensure schema constraints.

### DAG configuration includes:

- ⏰ Daily schedule (`@daily`)
- 🔁 Retry policy (`2 retries`, `2-minute delay`)
- ❌ No backfill (`catchup=False`)
- 🏷️ Tags for filtering and discoverability

## Testing & Validation

- Unit tests `(pytest`) validate:
   - Spotify API authentication logic.
   - Ingestion structure and expected fields.

- dbt tests (`schema.yml`) validate:
   - Column constraints (`not null`, `unique`)
   - Data format and referential integrity

## Environment Variables

- All sensitive data is stored in a `.env` file, which is excluded from version control:

```py
SPOTIPY_CLIENT_ID=
SPOTIPY_CLIENT_SECRET=
SPOTIPY_REDIRECT_URI=
```

## Getting Started

1. Clone the Repository

```py
git clone https://github.com/nathadriele/spotify-data-pipeline.git
cd spotify-data-pipeline
```

2. Configure Your Environment
- Create a `.env` file with your Spotify credentials.

3. Launch Services via Docker Compose

```py
docker-compose up --build
```

4. Trigger the DAG in Airflow
   - Access Airflow at `http://localhost:8080`
   - Trigger the `spotify_data_pipeline DAG`

##  Insights Available

🎷 Top artists and albums
🕐 Listening behavior by hour
⏱️ Track duration distribution
📈 Daily ingestion and transformation logs

## Highlights

- 📦 Containerized, modular, and reproducible
- 🧪 Fully tested with pytest and dbt
- 🔁 Orchestrated with Airflow, scheduled daily
- 📊 Dashboards and analytics via Metabase
- 🧱 Follows Medallion Architecture principles (Raw ➔ Staging ➔ Mart)

## Conclusion

This project consolidates the end-to-end implementation of a data pipeline using modern open-source tools. It serves as a reference for structuring scalable, testable, and well-orchestrated data workflows. The architecture can be adapted to multiple use cases involving data extraction, transformation, storage, and visualization.

## Contribution

Contributions are welcome! If you have ideas to improve the pipeline, fix bugs, or enhance documentation:
- Open an issue describing the enhancement or problem.
- Fork the repository and create a pull request.
- Make sure your code is well-structured and tested.
Let's collaborate to keep this project growing and useful for other data engineers!

## License

MIT License — see LICENSE file for details.
