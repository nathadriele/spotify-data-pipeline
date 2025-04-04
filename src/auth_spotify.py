# src/auth_spotify.py

import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load .env file
load_dotenv()

# Autenticação com escopo para músicas reproduzidas recentemente
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-recently-played"
))

# Teste: Buscar últimas 10 faixas reproduzidas
results = sp.current_user_recently_played(limit=10)

print("\n Últimas músicas reproduzidas:")
for idx, item in enumerate(results['items']):
    track = item['track']
    print(f"{idx + 1}. {track['name']} — {track['artists'][0]['name']}")
