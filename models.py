from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize the SQLAlchemy object
db = SQLAlchemy()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TKURadio(db.Model):
    __tablename__ = 'tkuradio'
    id = db.Column(db.Integer, primary_key=True)
    playlist_name = db.Column(db.String(200))
    spotify_playlist_id = db.Column(db.String(200))
    description = db.Column(db.Text)
    image = db.Column(db.String(200))  # optional thumbnail
    is_active = db.Column(db.Boolean, default=True)

class BackgroundMusic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String(255), unique=True, nullable=False)
    song_name = db.Column(db.String(255), nullable=True)
    file_name = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<BackgroundMusic {self.page_name} - {self.song_name}>"

class Upcoming(db.Model):
    __tablename__ = 'upcoming'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    folder = db.Column(db.String(100), nullable=True) 
    image = db.Column(db.String(300), nullable=True)
    description = db.Column(db.Text, nullable=True)

class Highlights(db.Model):
    __tablename__ = 'highlights'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    folder = db.Column(db.String(100), nullable=True) 
    image = db.Column(db.String(300), nullable=True)
    description = db.Column(db.Text, nullable=True)

class Recap(db.Model):
    __tablename__ = 'recap'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.Text, nullable=True)
    video = db.Column(db.String(300), nullable=False) 

class Memory(db.Model):
    __tablename__ = 'memory'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Memory {self.title}>'
  
class InTheNews(db.Model):
    __tablename__ = 'inthenews'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(255), nullable=True) 

    def __repr__(self):
        return f'<InTheNews {self.title}>'

class Discography(db.Model):
    __tablename__ = 'discography'

    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False) 
    album_name = db.Column(db.String(200), nullable=False)
    song_name = db.Column(db.String(200), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.String(10), nullable=False)
    popular = db.Column(db.Boolean, default=False)
    spotify_url = db.Column(db.String(255), nullable=True)
    apple_music_url = db.Column(db.String(255), nullable=True)
    youtube_url = db.Column(db.String(255), nullable=True)
    shazam_url = db.Column(db.String(255), nullable=True)
    pandora_url = db.Column(db.String(255), nullable=True)
    tidal_url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Discography {self.song_name}>'

class MusicVideo(db.Model):
    __tablename__ = 'musicvideo'

    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100), nullable=False)
    video_name = db.Column(db.String(255), nullable=False)
    youtube_url = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<MusicVideo {self.name}>'

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_logo = db.Column(db.String(255), nullable=False)
    app_name = db.Column(db.String(100), nullable=False, unique=True)
    android_link = db.Column(db.String(255), nullable=True)
    ios_link = db.Column(db.String(255), nullable=True)
    web_link = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Vote {self.app_name}>"
    
class Radio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_logo = db.Column(db.String(255), nullable=True) 
    station_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False) 
    station_link = db.Column(db.String(255), nullable=False) 
    request_link = db.Column(db.String(255), nullable=True) 
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Radio {self.station_name}>'
   
class SpotifyStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100), nullable=False)  # Added artist column
    image = db.Column(db.String(255), nullable=False)
    orig_song_name = db.Column(db.String(255), nullable=False)
    song_name = db.Column(db.String(255), nullable=False)
    total_streams = db.Column(db.Integer, nullable=False)
    popular = db.Column(db.Boolean, default=False)
    date = db.Column(db.String(10), nullable=False)
    
    def __repr__(self):
        return f'<ShazamStats {self.song_name} by {self.artist}>'
    
class YoutubeStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100), nullable=False)  # Added artist column
    image = db.Column(db.String(255), nullable=False)
    orig_song_name = db.Column(db.String(255), nullable=False)
    song_name = db.Column(db.String(255), nullable=False)
    view_count = db.Column(db.Integer, nullable=False)
    popular = db.Column(db.Boolean, default=False)
    date = db.Column(db.String(10), nullable=False)
    
    def __repr__(self):
        return f'<ShazamStats {self.song_name} by {self.artist}>'
    
class ShazamStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    orig_song_name = db.Column(db.String(255), nullable=False)
    song_name = db.Column(db.String(255), nullable=False)
    shazam_count = db.Column(db.Integer, nullable=False)
    popular = db.Column(db.Boolean, default=False)
    date = db.Column(db.String(10), nullable=False)
    
    def __repr__(self):
        return f'<ShazamStats {self.song_name} by {self.artist}>'
    
class Fanbase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logo = db.Column(db.String(255), nullable=True)
    fb_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=True)
    focus = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    x = db.Column(db.String(255), nullable=True)  # Social media links
    instagram = db.Column(db.String(255), nullable=True)
    facebook = db.Column(db.String(255), nullable=True)
    bluesky = db.Column(db.String(255), nullable=True)
    tiktok = db.Column(db.String(255), nullable=True)
    spotify = db.Column(db.String(255), nullable=True)
    applemusic = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Fanbase {self.fb_name}>"

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(255), nullable=True)  # Optional

    def __repr__(self):
        return f"<Project {self.title}>"

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    trending_tags = db.Column(db.String(100), nullable=True)
    trending_position = db.Column(db.String(100), nullable=True)
    link = db.Column(db.String(255), nullable=True) 

    def __repr__(self):
        return f'<Event {self.title}>'

class Promotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(100), nullable=False) 
    brand_name = db.Column(db.String(100), nullable=False)
    campaign_title = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String(500), nullable=False)
    video_url = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Event {self.campaign_title}>'
    
class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subpage = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=True)
    date_added = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f'<Banner {self.title}>'
    
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'
    
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default='Created')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class FanLetter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fanname = db.Column(db.String(255), nullable=True)  # Optional if image is provided
    image = db.Column(db.String(255), nullable=True)  # Image filename (stored in static/letters/)
    description = db.Column(db.Text, nullable=True)  # Optional if image is provided

    def __init__(self, fanname=None, image=None, description=None):
        if not fanname and not image:
            raise ValueError("Either an image or a title with description must be provided.")
        self.fanname = fanname
        self.image = image
        self.description = description