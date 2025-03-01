from flask import Flask, render_template, request, redirect, session, url_for, jsonify, current_app, send_from_directory
import os, secrets, random, calendar, subprocess
from models import db, BackgroundMusic, Upcoming, Memory, InTheNews, InTheNews_Spanish, Product, Discography, MusicVideo, Vote, Radio, SpotifyStats, YoutubeStats, ShazamStats, Fanbase, Banner, Project, Event, Promotion
from collections import defaultdict
from datetime import datetime

# Initialize the Flask app
app = Flask(__name__)

# Set a secret key for session management
app.secret_key = secrets.token_hex(16)

# Update the database URI to point to taekook.db inside the 'instance' folder
project_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(project_dir, 'instance', 'taekook.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy with the app
db.init_app(app)

@app.before_request
def force_https():
    if not current_app.debug and not request.is_secure:
        url = request.url.replace("http://", "https://", 1)
        return redirect(url, code=301)

@app.route('/')
def home():
    image_folder = os.path.join(app.static_folder, 'images/home')
    images = [f for f in os.listdir(image_folder) if f.endswith(('jpg', 'jpeg', 'png', 'gif'))]
    return render_template('01.home.html', images=images)

@app.route('/meet-tae')
def meet_tae():
    file_path = os.path.join(app.root_path, 'static', 'content', 'meet_tae.txt')
    with open(file_path, "r", encoding="utf-8") as file:
        tae_content = file.read()
    return render_template("09.01.meettae.html", tae_content=tae_content)

@app.route('/meet-koo')
def meet_koo():
    file_path = os.path.join(app.root_path, 'static', 'content', 'meet_koo.txt')
    with open(file_path, "r", encoding="utf-8") as file:
        koo_content = file.read()
    return render_template("09.02.meetkoo.html", koo_content=koo_content)

@app.route('/upcoming')
def upcoming():
    upcoming_events = Upcoming.query.order_by(Upcoming.date).all()
    for event in upcoming_events:
        if isinstance(event.date, str): 
            event.date = datetime.strptime(event.date, '%Y-%m-%d') 
    return render_template("02.upcoming.html", upcoming=upcoming_events)

@app.route('/memories')
def memories():
    video_dir = os.path.join(app.static_folder, 'videos')
    video_files = os.listdir(video_dir)

    memories_data = Memory.query.all()

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

    return render_template('03.memories.html', video_files=video_files,
                           timeline_data=timeline_data, 
                           calendar=calendar, 
                           formatted_years=formatted_years)

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
    return render_template('04.inthenews.html', inthenews=inthenews)

@app.route('/in-the-news/spanish')
def inthenews_spanish():
    spanish_news = InTheNews_Spanish.query.order_by(InTheNews_Spanish.date.desc()).all()
    return render_template("04.inthenews_spanish.html", inthenews_spanish=spanish_news)

@app.route('/vibe')
def vibe():
    song_names = [song.song_name for song in Discography.query.all() if song.song_name]
    taehyung_videos = db.session.query(MusicVideo).filter(MusicVideo.artist == 'Taehyung').all()
    jungkook_videos = db.session.query(MusicVideo).filter(MusicVideo.artist == 'Jungkook').all()
    random.shuffle(taehyung_videos)
    random.shuffle(jungkook_videos)
   
    return render_template('05.vibe.html', song_names=song_names, taehyung_videos=taehyung_videos, jungkook_videos=jungkook_videos)

@app.route('/projects')
def projects():
    projects = Project.query.all()  
    music = BackgroundMusic.query.filter_by(page_name='projects').first()
    song_file = music.file_name if music else "default.mp3"
    song_name = music.song_name if music else "Default Song"
    return render_template("06.projects.html", song_file=song_file, song_name=song_name, projects=projects)

@app.route("/guide")
def guide_page():
    return render_template("07.guide.html")

@app.route('/donating')
def donating():
    banners = Banner.query.filter_by(subpage='07.01.donating').all()
    return render_template('07.01.donating.html', banners=banners)

@app.route("/fanbases")
def fanbases():
    fanbases = Fanbase.query.all()
    banners = Banner.query.filter_by(subpage='07.02.fanbases').all()
    for fanbase in fanbases:
        print(fanbase.fb_name, fanbase.x, fanbase.instagram, fanbase.facebook)
    return render_template("07.02.fanbases.html", fanbases=fanbases, banners=banners)

@app.route("/streaming")
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

@app.route('/store')
def store():
    products = Product.query.all()
    selected_quantities = {}  
    return render_template('08.store.html', products=products, selected_quantities=selected_quantities)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = request.form['item']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])

    if 'cart' not in session:
        session['cart'] = {}

    if item in session['cart']:
        session['cart'][item]['quantity'] += quantity
    else:
        session['cart'][item] = {'quantity': quantity, 'price': price}

    session.modified = True 

    return jsonify({"message": "Item added to cart", "item": item, "quantity": quantity})

@app.route('/cart', methods=['POST', 'GET'])
def cart():
    cart_items = session.get('cart', {})
    
    if not cart_items:
        return render_template('08.01.cart.html', cart_items={}, total_price=0, message="Your cart is empty.")
    
    products = Product.query.all()
    
    if request.method == 'POST':
        for item in cart_items.keys():
            quantity = int(request.form.get(f"quantity_{item}", 0))
            if quantity > 0:
                cart_items[item]['quantity'] = quantity
            else:
                del cart_items[item] 

        session['cart'] = cart_items  
        session.modified = True 
        return redirect('/cart') 
    
    total_price = sum(item_details['quantity'] * item_details['price'] for item_details in cart_items.values())
    return render_template('08.01.cart.html', cart_items=cart_items, total_price=total_price, products=products)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)

