import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-recently-played"
))

results = sp.current_user_recently_played(limit=50)

data = [{
    "played_at": item["played_at"],
    "track_name": item["track"]["name"],
    "artist_name": item["track"]["artists"][0]["name"],
    "album_name": item["track"]["album"]["name"],
    "track_id": item["track"]["id"],
    "duration_ms": item["track"]["duration_ms"]
} for item in results["items"]]

df = pd.DataFrame(data)

conn = psycopg2.connect(
    host="localhost",
    database="spotify_db",
    user="spotify_user",
    password="spotify_pass",
    port=5432
)
cur = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS recent_tracks (
    played_at TIMESTAMP PRIMARY KEY,
    track_name TEXT,
    artist_name TEXT,
    album_name TEXT,
    track_id TEXT,
    duration_ms INTEGER
);
"""
cur.execute(create_table_query)

for _, row in df.iterrows():
    insert_query = """
    INSERT INTO recent_tracks (played_at, track_name, artist_name, album_name, track_id, duration_ms)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (played_at) DO NOTHING;
    """
    cur.execute(insert_query, (
        row["played_at"],
        row["track_name"],
        row["artist_name"],
        row["album_name"],
        row["track_id"],
        row["duration_ms"]
    ))

conn.commit()
cur.close()
conn.close()

print("Dados salvos com sucesso no PostgreSQL!")
