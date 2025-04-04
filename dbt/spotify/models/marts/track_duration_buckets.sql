-- models/marts/track_duration_buckets.sql

with base as (
    select * from {{ ref('stg_recent_tracks') }}
),

categorized as (
    select
        track_name,
        artist_name,
        duration_sec,
        case
            when duration_sec < 120 then 'short (<2min)'
            when duration_sec between 120 and 240 then 'medium (2-4min)'
            else 'long (>4min)'
        end as duration_category
    from base
)

select
    duration_category,
    count(*) as total_tracks
from categorized
group by duration_category
order by total_tracks desc
