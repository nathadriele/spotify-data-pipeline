-- models/marts/listening_by_hour.sql

with base as (
    select * from {{ ref('stg_recent_tracks') }}
),

by_hour as (
    select
        extract(hour from played_at) as hour_of_day,
        count(*) as total_tracks
    from base
    group by hour_of_day
    order by hour_of_day
)

select * from by_hour
