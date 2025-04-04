-- models/marts/top_albums.sql

with base as (
    select * from {{ ref('stg_recent_tracks') }}
),

album_agg as (
    select
        album_name,
        count(*) as total_tracks,
        round(avg(duration_sec), 2) as avg_duration_sec
    from base
    group by album_name
    order by total_tracks desc
)

select * from album_agg
