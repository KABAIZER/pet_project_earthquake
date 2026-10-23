{% docs usgs__earthquakes %}
Таблица public.earthquakes в Postgres (postgres_dwh): землетрясения магнитудой 2.5 и выше из API USGS. Загружается DAG'ом earthquakes_to_dwh (API → MinIO raw → Postgres, upsert по event_id).
{% enddocs %}

{% docs earthquakes_stg__earthquakes %}
Staging над источником usgs.earthquakes: переименование полей, приведение времени к дате в UTC, булев флаг цунами. Отбрасывает строки без event_id или magnitude. Эфемерная модель: в базе и в MinIO не хранится, встраивается как CTE.
{% enddocs %}

{% docs earthquakes_dbt_int__enriched %}
Обогащённые события: к полям staging добавлены region, magnitude_class и depth_class. Эфемерная модель, отдельных файлов не создаёт.
{% enddocs %}

{% docs earthquakes_dbt_mart__daily %}
Витрина по дням: число событий, средняя и максимальная магнитуда, число сильных событий и событий с флагом цунами. Одна строка на день. Хранится как parquet в MinIO: при target prod в бакете prod, при любом другом в бакете dev.
{% enddocs %}

{% docs earthquakes_dbt_mart__by_region %}
Витрина по регионам: число событий, средняя и максимальная магнитуда, время последнего события. Одна строка на регион. Хранится как parquet в MinIO: при target prod в бакете prod, при любом другом в бакете dev.
{% enddocs %}