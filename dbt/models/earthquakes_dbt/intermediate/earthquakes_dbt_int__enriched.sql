select
    *,
    trim(regexp_extract(place, '[^,]*$')) as region,
    case
        when magnitude < 3 then 'micro'
        when magnitude < 4 then 'minor'
        when magnitude < 5 then 'light'
        when magnitude < 6 then 'moderate'
        when magnitude < 7 then 'strong'
        else 'major'
    end as magnitude_class,
    case
        when depth_km is null then null
        when depth_km < 70 then 'shallow'
        when depth_km < 300 then 'intermediate'
        else 'deep'
    end as depth_class
from {{ ref('earthquakes_stg__earthquakes') }}