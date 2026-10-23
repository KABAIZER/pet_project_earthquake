with source as (
    select * from {{ source('usgs', 'earthquakes') }}
)

select
    event_id,
    event_time                              as event_at,
    (event_time at time zone 'UTC')::date   as event_date,
    magnitude,
    mag_type,
    place,
    longitude,
    latitude,
    depth_km,
    coalesce(tsunami, 0) = 1                as is_tsunami_flagged,
    url,
    updated_at
from source
where event_id is not null
  and magnitude is not null