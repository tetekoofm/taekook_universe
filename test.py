from app import app, db
from models import TKURadio

with app.app_context():
    stations = TKURadio.query.all()
    print(len(stations))
    for s in stations:
        print(s.playlist_name, s.spotify_playlist_id)