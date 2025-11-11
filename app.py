from flask import Flask, render_template, request, Response, redirect, session, url_for, jsonify, current_app, send_from_directory, send_file
import os, secrets, random, calendar, subprocess, base64, requests, json
from models import db, TKURadio, BackgroundMusic, Upcoming, Highlights, Recap, Memory, InTheNews, Product, Discography, MusicVideo, Vote, Radio, SpotifyStats, YoutubeStats, ShazamStats, Fanbase, Banner, Project, Event, Promotion, FanLetter
from collections import defaultdict
from datetime import datetime
from flask_wtf import CSRFProtect
from scraper.naver_scraper import scrape_naver_blog

# Initialize the Flask app
app = Flask(__name__)

csrf = CSRFProtect(app)

# Set a secret key for session management
app.secret_key = secrets.token_hex(16)

# Update the database URI to point to taekook.db inside the 'instance' folder
project_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(project_dir, 'instance', 'taekook.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy with the app
db.init_app(app)


# ----------------- Spotify Credentials -----------------
def get_spotify_credentials():
    required = [
        "SPOTIFY_CLIENT_ID",
        "SPOTIFY_CLIENT_SECRET",
        "SPOTIFY_SCOPE"
    ]
    if all(os.getenv(var) for var in required):
        creds = {var: os.getenv(var) for var in required}
        # Redirect URI is dynamic based on environment
        if os.environ.get("FLASK_ENV") == "development":
            creds["SPOTIFY_REDIRECT_URI"] = "http://localhost:8888/callback"
        else:
            creds["SPOTIFY_REDIRECT_URI"] = os.getenv("SPOTIFY_REDIRECT_URI")
        return creds
    # Fallback to local taekook_spotify.json
    try:
        with open("taekook_spotify.json") as f:
            creds = json.load(f)
        if os.environ.get("FLASK_ENV") == "development":
            creds["SPOTIFY_REDIRECT_URI"] = "http://localhost:8888/callback"
        return creds
    except FileNotFoundError:
        raise RuntimeError("No Spotify credentials found. Set env vars or provide taekook_spotify.json.")

spotify_creds = get_spotify_credentials()
print("Loaded Spotify creds:", spotify_creds)
SPOTIFY_CLIENT_ID = spotify_creds["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = spotify_creds["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = spotify_creds["SPOTIFY_REDIRECT_URI"]
SPOTIFY_SCOPE = spotify_creds["SPOTIFY_SCOPE"]

def get_playlists_with_images(playlists, access_token):
    for pl in playlists:
        if not pl.image and access_token:
            url = f"https://api.spotify.com/v1/playlists/{pl.spotify_playlist_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            if response.ok:
                data = response.json()
                if data.get("images"):
                    pl.image = data['images'][0]['url']
    return playlists

@app.route("/login")
def login():
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={SPOTIFY_CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI}"
        f"&scope={SPOTIFY_SCOPE}"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "No code returned from Spotify"

    # Exchange code for access token
    token_url = "https://accounts.spotify.com/api/token"
    response = requests.post(token_url, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    })
    token_data = response.json()
    access_token = token_data.get("access_token")
    if not access_token:
        return f"Error retrieving token: {token_data}"

    session["access_token"] = access_token
    return redirect(url_for("tkuradio"))

@app.route('/tkuradio')
def tkuradio():
    access_token = session.get("access_token")
    playlists = TKURadio.query.filter_by(is_active=True).all()
    playlists = get_playlists_with_images(playlists, access_token)
    banners = Banner.query.filter_by(subpage='12.tkuradio').all()
    return render_template(
        "12.tkuradio.html",
        playlists=playlists,
        banners=banners,
        access_token=access_token or ""  # ensure JS sees "" if not logged in
    )

@app.before_request
def force_https():
    if not current_app.debug and not request.is_secure:
        url = request.url.replace("http://", "https://", 1)
        return redirect(url, code=301)

@app.route('/favicon.png')
def favicon():
    return send_from_directory('static', 'favicon.png', mimetype='image/png')

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    return send_file(os.path.join(app.root_path, 'static', 'sitemap.xml'), mimetype='application/xml')

@app.route('/home_soon')
def home_soon():
    image_folder = os.path.join(app.static_folder, 'images/home')
    images = [f for f in os.listdir(image_folder) if f.endswith(('jpg', 'jpeg', 'png', 'gif', 'webp', '.mp4'))]
    music = BackgroundMusic.query.filter_by(page_name='home').first()
    song_file = music.file_name if music else "your_eyes_tell.mp3"
    song_name = music.song_name if music else "Default Song"
    return render_template('01.home_soon.html', song_file=song_file, song_name=song_name, images=images)

@app.route('/')
def home():
    image_folder = os.path.join(app.static_folder, 'images/home/pictureoftheday')
    images = [f for f in os.listdir(image_folder) if f.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4'))]
    random.shuffle(images)
    # selected_media = images[:6]  # ✅ correct list slicing
    music = BackgroundMusic.query.filter_by(page_name='home').first()
    song_file = music.file_name if music else "your_eyes_tell.mp3"
    song_name = music.song_name if music else "Your Eyes Tell"
    return render_template('01.home.html', song_file=song_file, song_name=song_name, images=images)

@app.route('/meet-tae')
def meet_tae():
    music = BackgroundMusic.query.filter_by(page_name='meet tae').first()
    song_file = music.file_name if music else "default.mp3"
    song_name = music.song_name if music else "Default Song"
    return render_template("10.01.meettae.html", song_file=song_file, song_name=song_name)

@app.route('/meet-koo')
def meet_koo():
    music = BackgroundMusic.query.filter_by(page_name='meet koo').first()
    song_file = music.file_name if music else "default.mp3"
    song_name = music.song_name if music else "Default Song"
    return render_template("10.02.meetkoo.html", song_file=song_file, song_name=song_name)

@app.route('/termsandconditions')
def termsandconditions():
    return render_template("10.03.termsandconditions.html")

@app.route('/upcoming')
def upcoming():
    upcoming_events = Upcoming.query.all()
    music = BackgroundMusic.query.filter_by(page_name='upcoming').first()
    song_file = music.file_name if music else "default.mp3"
    song_name = music.song_name if music else "Default Song"
    for event in upcoming_events:
        if isinstance(event.date, str): 
            event.date = datetime.strptime(event.date, '%Y-%m-%d') 
    return render_template("02.01.upcoming.html", upcoming=upcoming_events, song_file=song_file, song_name=song_name)

@app.route('/highlights')
def highlights():
    highlights_events = Highlights.query.all()
    music = BackgroundMusic.query.filter_by(page_name='highlights').first()
    song_file = music.file_name if music else "default.mp3"
    song_name = music.song_name if music else "Default Song"
    for event in highlights_events:
        if isinstance(event.date, str): 
            event.date = datetime.strptime(event.date, '%Y-%m-%d') 
    return render_template("02.02.highlights.html", highlights=highlights_events, song_file=song_file, song_name=song_name)

@app.route('/recap')
def recap():
    recaps = Recap.query.order_by(Recap.date.desc()).all()
    music = BackgroundMusic.query.filter_by(page_name='highlights').first()
    song_file = music.file_name if music else "default.mp3"
    song_name = music.song_name if music else "Default Song"
    return render_template("02.03.recap.html", recaps=recaps, song_file=song_file, song_name=song_name)

@app.route('/memories')
def memories():
    video_dir = os.path.join(app.static_folder, 'videos')
    video_files = os.listdir(video_dir)

    memories_data = Memory.query.all()
    music = BackgroundMusic.query.filter_by(page_name='memories').first()
    song_file = music.file_name if music else "default.mp3"
    song_name = music.song_name if music else "Default Song"
    timeline_data = defaultdict(lambda: defaultdict(list))

    for memory in memories_data:
        year, month, day = map(int, memory.date.split('-'))  
        timeline_data[year][month].append({
            'id': memory.id,
            'title': memory.title,
            'date': f'{year}-{month:02}-{day:02}',  
            'image': memory.image,
            'description': memory.description,
        })

    for year in range(2013, 2025):  
        if year not in timeline_data:
            timeline_data[year] = {}
        for month in range(1, 13): 
            timeline_data[year].setdefault(month, [])

        # Sort months chronologically
        timeline_data[year] = {
            month: timeline_data[year][month]
            for month in sorted(timeline_data[year])
        }

    formatted_years = {year: str(year)[-2:] for year in timeline_data.keys()}

    # return render_template('03.memories.html', video_files=video_files,
    #                        timeline_data=timeline_data, 
    #                        calendar=calendar, 
    #                        formatted_years=formatted_years)

    return render_template('03.memories_soon.html', song_file=song_file, song_name=song_name)

@app.route('/memories_data')
def memories_data():
    memories_data = Memory.query.all()
    timeline_data = defaultdict(lambda: defaultdict(list))

    for memory in memories_data:
        year, month, day = map(int, memory.date.split('-'))
        timeline_data[year][month].append({
            'id': memory.id,
            'title': memory.title,
            'date': f'{year}-{month:02}-{day:02}',
            'artist': memory.artist,
            'image': memory.image,
            'description': memory.description
        })

    return jsonify(timeline_data)

@app.route('/memories_galaxy')
def memories_galaxy():
    memories_data = Memory.query.all()
    music = BackgroundMusic.query.filter_by(page_name='memories').first()
    song_file = music.file_name if music else "default.mp3"
    song_name = music.song_name if music else "Default Song"
    events = []
    for memory in memories_data:
        year, month, day = map(int, memory.date.split('-'))
        month_name = memory.date.split('-')[1]
        events.append({
            "year": year,
            "month": month_name,
            "title": memory.title,
            "description": memory.description,
            "image": memory.image,
            "artist": memory.artist,
            "date": memory.date
        })

    return render_template('03.memories.html', events=events, song_file=song_file, song_name=song_name)

@app.route('/get-event-details/<int:event_id>', methods=['GET'])
def get_event_details(event_id):
    event = Memory.query.get(event_id)
    if event:
        return jsonify({
            'title': event.title,
            'image': url_for('static', filename=f'images/{event.image}'),
            'description': event.description,
            'date': event.date
        })
    else:
        return jsonify({'error': 'Event not found'}), 404

@app.route('/inthenews')
def inthenews():
    inthenews = InTheNews.query.order_by(InTheNews.date.desc()).all()
    music = BackgroundMusic.query.filter_by(page_name='inthenews').first()
    song_file = music.file_name if music else "default.mp3"
    song_name = music.song_name if music else "Default Song"
    return render_template("04.inthenews.html", song_file=song_file, song_name=song_name, inthenews=inthenews)

@app.route('/vibe')
def vibe():
    song_names = [song.song_name for song in Discography.query.all() if song.song_name]
    taehyung_videos = db.session.query(MusicVideo).filter(MusicVideo.artist == 'Taehyung').all()
    jungkook_videos = db.session.query(MusicVideo).filter(MusicVideo.artist == 'Jungkook').all()
    random.shuffle(taehyung_videos)
    random.shuffle(jungkook_videos)
    music = BackgroundMusic.query.filter_by(page_name='vibe').first()
    song_file = music.file_name if music else "default.mp3"
    song_name = music.song_name if music else "Default Song"
    return render_template("05.vibe.html", song_names=song_names, song_file=song_file, song_name=song_name, taehyung_videos=taehyung_videos, jungkook_videos=jungkook_videos)
    
@app.route('/projects')
def projects():
    projects = Project.query.all()  
    music = BackgroundMusic.query.filter_by(page_name='projects').first()
    song_file = music.file_name if music else "default.mp3"
    song_name = music.song_name if music else "Default Song"
    return render_template("06.projects.html", song_file=song_file, song_name=song_name, projects=projects)

@app.route('/pride')
def pride():
    return render_template("11.pride.html")

@app.route('/guide')
def guide():
    return render_template("07.guide.html")

@app.route('/donating')
def donating():
    banners = Banner.query.filter_by(subpage='07.01.donating').all()
    return render_template('07.01.donating.html', banners=banners)

@app.route('/fanbases')
def fanbases():
    fanbases = Fanbase.query.all()
    banners = Banner.query.filter_by(subpage='07.02.fanbases').all()
    for fanbase in fanbases:
        print(fanbase.fb_name, fanbase.x, fanbase.instagram, fanbase.facebook)
    return render_template("07.02.fanbases.html", fanbases=fanbases, banners=banners)

@app.route('/streaming')
def streaming():
    trending_tracks = Discography.query.filter_by(popular=1).all()
    banners = Banner.query.filter_by(subpage='07.03.streaming').all()
    return render_template('07.03.streaming.html', trending_tracks=trending_tracks, banners=banners)

@app.route('/spotifystats')
def spotifystats():
    stats = SpotifyStats.query.all()
    date_as_of = stats[0].date if stats else None
    return render_template('spotifystats.html', stats=stats, date_as_of=date_as_of)

@app.route('/youtubestats')
def youtubestats():
    stats = YoutubeStats.query.all()
    date_as_of = stats[0].date if stats else None
    return render_template('youtubestats.html', stats=stats, date_as_of=date_as_of)

@app.route('/buying')
def buying():
    banners = Banner.query.filter_by(subpage='07.04.buying').all()
    return render_template('07.04.buying.html', banners=banners)

@app.route('/voting')
def voting():
    banners = Banner.query.filter_by(subpage='07.05.voting').all()
    vote_apps = Vote.query.all()  # Fetch all voting apps
    return render_template('07.05.voting.html', banners=banners, vote_apps=vote_apps)


@app.route('/radio')
def radio():
    radio_stations = Radio.query.all() 
    banners = Banner.query.filter_by(subpage='07.06.radio').all()
    return render_template('07.06.radio.html', radio_stations=radio_stations, banners=banners)

@app.route('/shazam')
def shazam():
    shazam_stats = ShazamStats.query.all()
    popular_tracks = ShazamStats.query.filter_by(popular=True).all()  # Only popular tracks
    date_as_of = shazam_stats[0].date if shazam_stats else None
    banners = Banner.query.filter_by(subpage='07.07.shazam').all()
    return render_template('07.07.shazam.html', shazam_stats=shazam_stats, popular_tracks=popular_tracks, date_as_of=date_as_of, banners=banners)

@app.route('/shazamstats')
def shazamstats():
    stats = ShazamStats.query.all()
    date_as_of = stats[0].date if stats else None
    return render_template('shazamstats.html', stats=stats, date_as_of=date_as_of)

@app.route('/brandreputation')
def brandreputation():
    banners = Banner.query.filter_by(subpage='07.08.brand_reputation').all()
    return render_template('07.08.brand_reputation.html', banners=banners)

@app.route('/promotions')
def promotions():
    ads = Promotion.query.order_by(Promotion.year.desc()).all()
    banners = Banner.query.filter_by(subpage='07.09.promotions').all()
    return render_template('07.09.promotions.html', ads=ads)

@app.route('/endorsements')
def endorsements():
    banners = Banner.query.filter_by(subpage='07.09.endorsements').all()
    return render_template('07.09.endorsements.html', banners=banners)

@app.route('/events')
def events():
    events = Event.query.all()
    banners = Banner.query.filter_by(subpage='07.10.events').all()
    return render_template('07.10.events.html', banners=banners, events=events)

@app.route('/reporting')
def reporting():
    banners = Banner.query.filter_by(subpage='07.11.reporting').all()
    return render_template('07.11.reporting.html', banners=banners)

@app.route('/fanletters')
def fan_letters_page():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    fan_letters = FanLetter.query.paginate(page=page, per_page=per_page, error_out=False)
    music = BackgroundMusic.query.filter_by(page_name='fan letters').first()
    song_file = music.file_name if music else "default.mp3"
    song_name = music.song_name if music else "Default Song"
    return render_template('09.fanletters.html', song_file=song_file, song_name=song_name, fan_letters=fan_letters)

## GAMES ##########################################################################################################

@app.route('/games')
def games():
    return render_template('13.games.html')

LEADERBOARD_FILE = 'leaderboard.json'  # or full path if outside project folder


# ---------------------- HALLOWEEN HUNT ----------------------
# Required as we have if clause in base nav and sub nav remplates
@app.context_processor
def inject_halloween_flag():
    # make this True during the Halloween event
    return dict(halloween_hunt_active=True)

@app.route("/christmas_delivery")
def christmas_delivery():
    return render_template("13.01.christmas_delivery.html")

@app.route("/halloween-hunt")
def halloween_hunt():
    return render_template("13.01.halloween_hunt.html")

@app.route("/halloween-special")
def halloween_special():
    return render_template("13.01.halloween_special.html")

@app.route('/guesswithemoji')
def guess_song_emoji():
    return render_template('13.02.guess_song_emoji.html')

@app.route('/guesswithlyrics')
def guess_song_lyrics():
    return render_template('13.03.guess_song_lyrics.html')

@app.route('/guesswithscrambled')
def guess_song_scrambled():
    return render_template('13.04.guess_song_scrambled.html')

# Load leaderboard JSON
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return {}
    with open(LEADERBOARD_FILE, 'r') as f:
        return json.load(f)

# Save leaderboard JSON
def save_leaderboard(data):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/submit_score', methods=['POST'])
@csrf.exempt
def submit_score():
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "No JSON received"}), 400

    game = payload.get('game')
    username = payload.get('username', 'Anonymous')
    score = payload.get('score', 0)

    if not game:
        return jsonify({"error": "Game name required"}), 400

    # Load existing data
    data = load_leaderboard()
    if game not in data:
        data[game] = []

    # Append and sort
    data[game].append({"username": username, "score": score})
    data[game] = sorted(data[game], key=lambda x: x['score'], reverse=True)[:10]

    # Save back
    save_leaderboard(data)

    return jsonify({"success": True, "leaderboard": data[game]})

# Fetch leaderboard
@app.route('/leaderboard/<game_name>')
def get_leaderboard(game_name):
    data = load_leaderboard()
    return jsonify(data.get(game_name, []))

## GAMES ##########################################################################################################

@app.after_request
def add_headers(response):
    response.headers["Permissions-Policy"] = "compute-pressure=()"
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8888)