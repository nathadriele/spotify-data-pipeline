# tests/test_ingestion.py

import os
import pytest
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

@pytest.fixture
def spotify_client():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope="user-read-recently-played"
        )
    )
    return sp

def test_authentication(spotify_client):
    me = spotify_client.me()
    assert "id" in me
    assert "display_name" in me

def test_recent_tracks_structure(spotify_client):
    results = spotify_client.current_user_recently_played(limit=5)
    assert "items" in results
    for item in results["items"]:
        track = item["track"]
        assert "name" in track
        assert "artists" in track
