select
    event_date                                  as day,
    count(*)                                    as events,
    round(avg(magnitude), 2)                    as avg_magnitude,
    max(magnitude)                              as max_magnitude,
    count(*) filter (where magnitude >= 5)      as moderate_plus_events,
    count(*) filter (where is_tsunami_flagged)  as tsunami_flagged_events
from {{ ref('earthquakes_dbt_int__enriched') }}
group by 1