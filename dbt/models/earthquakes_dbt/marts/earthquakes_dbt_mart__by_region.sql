select
    region,
    count(*)                    as events,
    round(avg(magnitude), 2)    as avg_magnitude,
    max(magnitude)              as max_magnitude,
    max(event_at)               as last_event_at
from {{ ref('earthquakes_dbt_int__enriched') }}
group by 1