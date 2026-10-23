import json
from datetime import datetime, timedelta, timezone

import requests
from airflow.decorators import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook

API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
MIN_MAGNITUDE = 2.5
BUCKET = "raw"
S3_CONN_ID = "minio_s3"
DWH_CONN_ID = "dwh"


def to_utc_iso(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()


@dag(
    dag_id="earthquakes_to_dwh",
    start_date=datetime(2026, 9, 1),
    schedule="@daily",
    catchup=True,
    max_active_runs=1,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["etl", "api", "usgs"],
)
def earthquakes_to_dwh():

    @task
    def extract_to_raw(data_interval_start=None, data_interval_end=None) -> str:
        """API -> MinIO. Сохраняем ответ как есть, без преобразований."""
        params = {
            "format": "geojson",
            "starttime": data_interval_start.strftime("%Y-%m-%dT%H:%M:%S"),
            "endtime": data_interval_end.strftime("%Y-%m-%dT%H:%M:%S"),
            "minmagnitude": MIN_MAGNITUDE,
            "orderby": "time-asc",
        }
        resp = requests.get(API_URL, params=params, timeout=60)
        resp.raise_for_status()

        day = data_interval_start.strftime("%Y-%m-%d")
        key = f"earthquakes/dt={day}/earthquakes.json"
        S3Hook(aws_conn_id=S3_CONN_ID).load_string(
            string_data=resp.text, key=key, bucket_name=BUCKET, replace=True
        )
        return key  # по XCom передаём только путь, не сами данные

    @task
    def load_to_dwh(key: str) -> None:
        """MinIO -> Postgres."""
        raw = S3Hook(aws_conn_id=S3_CONN_ID).read_key(key=key, bucket_name=BUCKET)
        features = json.loads(raw)["features"]

        rows = []
        for f in features:
            p = f["properties"]
            lon, lat, depth = f["geometry"]["coordinates"]
            rows.append(
                {
                    "event_id": f["id"],
                    "event_time": to_utc_iso(p["time"]),
                    "magnitude": p["mag"],
                    "mag_type": p["magType"],
                    "place": p["place"],
                    "longitude": lon,
                    "latitude": lat,
                    "depth_km": depth,
                    "tsunami": p["tsunami"],
                    "url": p["url"],
                    "updated_at": to_utc_iso(p["updated"]),
                }
            )

        hook = PostgresHook(postgres_conn_id=DWH_CONN_ID)
        hook.run(
            """
            CREATE TABLE IF NOT EXISTS earthquakes (
                event_id   TEXT PRIMARY KEY,
                event_time TIMESTAMPTZ,
                magnitude  NUMERIC,
                mag_type   TEXT,
                place      TEXT,
                longitude  DOUBLE PRECISION,
                latitude   DOUBLE PRECISION,
                depth_km   DOUBLE PRECISION,
                tsunami    INTEGER,
                url        TEXT,
                updated_at TIMESTAMPTZ
            )
            """
        )
        if not rows:
            print(f"В {key} событий нет")
            return

        fields = list(rows[0].keys())
        hook.insert_rows(
            table="earthquakes",
            rows=[tuple(r[k] for k in fields) for r in rows],
            target_fields=fields,
            replace=True,
            replace_index=["event_id"],
        )
        print(f"Загружено событий из {key}: {len(rows)}")

    load_to_dwh(extract_to_raw())


earthquakes_to_dwh()