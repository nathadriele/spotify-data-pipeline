-- models/marts/top_artists.sql

with base as (
    select * from {{ ref('stg_recent_tracks') }}
),

artist_agg as (
    select
        artist_name,
        count(*) as total_tracks,
        round(avg(duration_sec), 2) as avg_duration_sec
    from base
    group by artist_name
    order by total_tracks desc
)

select * from artist_agg
