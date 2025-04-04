-- models/staging/stg_recent_tracks.sql

with source as (

    select *
    from public.recent_tracks

),

renamed as (

    select
        played_at,
        track_name,
        artist_name,
        album_name,
        track_id,
        duration_ms / 1000.0 as duration_sec
    from source

)

select * from renamed
