CREATE OR REPLACE TABLE marts.earthquakes_daily
ENGINE = MergeTree ORDER BY tuple()
AS SELECT * FROM s3('http://minio:9000/dev/earthquakes_dbt/mart/earthquakes_dbt_mart__daily.parquet', 'minioadmin', 'minioadmin', 'Parquet');

CREATE OR REPLACE TABLE marts.earthquakes_by_region
ENGINE = MergeTree ORDER BY tuple()
AS SELECT * FROM s3('http://minio:9000/dev/earthquakes_dbt/mart/earthquakes_dbt_mart__by_region.parquet', 'minioadmin', 'minioadmin', 'Parquet');