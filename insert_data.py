import pandas as pd
from models import db, BackgroundMusic, Upcoming,  Recap, Memory, InTheNews, InTheNews_Spanish, Product, Discography, MusicVideo, Vote, Radio, Fanbase, SpotifyStats, YoutubeStats, ShazamStats, Banner, Project, Event, Promotion, FanLetter
from app import app
from datetime import datetime, time

def insert_data_from_excel():
    excel_file = 'taekook_universe.xlsx'

    with app.app_context():

        music_df = pd.read_excel(excel_file, sheet_name='Background Music')

        for _, row in music_df.iterrows():
            existing = BackgroundMusic.query.filter_by(page_name=row['page_name']).first()

            if not existing:
                music_entry = BackgroundMusic(
                    page_name=row['page_name'],
                    song_name=row['song_name'],
                    file_name=row['file_name']
                )
                db.session.add(music_entry)

        db.session.commit()
        print("Background Music updated from Excel!")

        upcoming_df = pd.read_excel(excel_file, sheet_name='Upcoming')
        upcoming_df['date'] = pd.to_datetime(upcoming_df['date'], errors='coerce')

        # Ensure no NaT values before formatting
        upcoming_df = upcoming_df.dropna(subset=['date'])

        # Convert to string format for database insertion
        upcoming_df['date'] = upcoming_df['date'].dt.strftime('%Y-%m-%d')

        for _, row in upcoming_df.iterrows():
            existing = Upcoming.query.filter_by(
                date=row['date'], 
                artist=row['artist'], 
                title=row['title']
            ).first()
            if not existing:
                upcoming = Upcoming(
                    date=row['date'],
                    artist=row['artist'],
                    title=row['title'],
                    image=row['image'],
                    description=row['description']
                )
                db.session.add(upcoming)

        db.session.commit()
        print("Upcoming Events updated from Excel!")

        recap_df = pd.read_excel(excel_file, sheet_name='Recap')
        recap_df['date'] = pd.to_datetime(recap_df['date'], errors='coerce')
        recap_df = recap_df.dropna(subset=['date'])

        for _, row in recap_df.iterrows():
            formatted_date = row['date'].strftime('%Y-%m-%d')  # Convert to str

            existing = Recap.query.filter_by(
                date=formatted_date,
                title=row['title']
            ).first()

            if not existing:
                recap = Recap(
                    date=formatted_date,
                    title=row['title'],
                    caption=row['caption'],
                    video=row['filename']
                )
                db.session.add(recap)


        db.session.commit()
        print("Recap videos updated from Excel!")

        memory_df = pd.read_excel(excel_file, sheet_name='Memory')
        memory_df['date'] = pd.to_datetime(memory_df['date'], errors='coerce')
        memory_df = memory_df.dropna(subset=['date'])
        memory_df['date'] = memory_df['date'].dt.strftime('%Y-%m-%d')
        for _, row in memory_df.iterrows():
            existing = Memory.query.filter_by(
                date=row['date'], 
                artist=row['artist'], 
                title=row['title']
            ).first()
            if not existing:
                memory = Memory(
                    date=row['date'],
                    artist=row['artist'],
                    title=row['title'],
                    image=row['image'],
                    description=row['description']
                )
                db.session.add(memory)
        db.session.commit()
        print("Memories updated from Excel!")

        inthenews_df = pd.read_excel(excel_file, sheet_name='In The News')
        inthenews_df['date'] = inthenews_df['date'].dt.strftime('%Y-%m-%d')

        for _, row in inthenews_df.iterrows():
            existing = InTheNews.query.filter_by(
                date=row['date'], 
                artist=row['artist'], 
                title=row['title']
            ).first()
            
            if not existing:
                inthenews = InTheNews(
                    date=row['date'],
                    artist=row['artist'],
                    title=row['title'],
                    image=row['image'],
                    description=row['description'],
                    link=row['link']
                )
                db.session.add(inthenews)

        db.session.commit()
        print("InTheNews updated from Excel!")

        inthenews_spanish_df = pd.read_excel(excel_file, sheet_name='Spanish News')
        inthenews_spanish_df['date'] = inthenews_spanish_df['date'].dt.strftime('%Y-%m-%d')

        for _, row in inthenews_spanish_df.iterrows():
            existing = InTheNews_Spanish.query.filter_by(
                date=row['date'], 
                artist=row['artist'], 
                title=row['title']
            ).first()
            
            if not existing:
                inthenews_spanish = InTheNews_Spanish(
                    date=row['date'],
                    artist=row['artist'],
                    title=row['title'],
                    image=row['image'],
                    description=row['description'],
                    link=row['link']
                )
                db.session.add(inthenews_spanish)

        db.session.commit()
        print("InTheNews_Spanish updated from Excel!")

        discography_df = pd.read_excel(excel_file, sheet_name='Discography')

        for _, row in discography_df.iterrows():
            popular = row['popular'] if 'popular' in row else 0
            existing = Discography.query.filter_by(
                artist=row['artist'],
                album_name=row['album_name'],
                song_name=row['song_name'],
                popular=popular
            ).first()

            if not existing:
                duration_str = str(row['duration'])
                discography = Discography(
                    artist=row['artist'],
                    image=row.get('image', None), 
                    album_name=row['album_name'],
                    song_name=row['song_name'],
                    release_date=row['release_date'],
                    duration=duration_str,
                    popular=popular,
                    spotify_url=row.get('spotify_url', None),
                    apple_music_url=row.get('apple_music_url', None),
                    youtube_url=row.get('youtube_url', None),
                    shazam_url=row.get('shazam_url', None),
                    pandora_url=row.get('pandora_url', None),
                    tidal_url=row.get('tidal_url', None)
                )
                db.session.add(discography)

        db.session.commit()
        print("Discography updated from Excel!")

        music_video_df = pd.read_excel(excel_file, sheet_name='MusicVideo')
        for _, row in music_video_df.iterrows():
            existing = MusicVideo.query.filter_by(
                artist=row['artist'],
                video_name=row['video_name'],
                youtube_url=row['youtube_url']
            ).first()
            if not existing:
                video = MusicVideo(
                    artist=row['artist'],
                    video_name=row['video_name'],
                    youtube_url=row['youtube_url']
                )
                db.session.add(video)
        db.session.commit()
        print("Music Videos updated from Excel!")

        vote_df = pd.read_excel(excel_file, sheet_name="Vote")
        for _, row in vote_df.iterrows():
            existing = Vote.query.filter_by(app_name=row['app_name']).first()

            if not existing:
                vote = Vote(
                    app_logo=row['app_logo'],
                    app_name=row['app_name'],
                    android_link=row['android_link'],
                    ios_link=row['ios_link'],
                    web_link=row['web_link']
                )
                db.session.add(vote)

        db.session.commit()
        print("Vote data updated from Excel!")

        radio_df = pd.read_excel(excel_file, sheet_name="Radio")
        for _, row in radio_df.iterrows():
            existing = Radio.query.filter_by(station_name=row['station_name']).first()

            if not existing:
                radio = Radio(
                    station_name=row['station_name'],
                    location=row['location'],
                    station_logo=row['station_logo'],
                    station_link=row['station_link'],
                    request_link=row['request_link'],
                    description=row['description']
                )
                db.session.add(radio)

        db.session.commit()
        print("Radio stations data updated from Excel!")

        spotify_df = pd.read_excel(excel_file, sheet_name="spotifystats", dtype={'image': str})
        data_as_of = pd.read_excel(excel_file, sheet_name="spotifystats", header=None).iloc[0, 8]  # I1 is in row 0, column 8 (0-indexed)
       
        # Convert date format
        if isinstance(data_as_of, datetime):
            data_as_of = data_as_of.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(data_as_of, time):
            today = datetime.today()
            data_as_of = datetime.combine(today, data_as_of).strftime('%Y-%m-%d %H:%M:%S')
        else:
            data_as_of = datetime.strptime(data_as_of, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        # Insert into database
        for _, row in spotify_df.iterrows():
            popular = row['popular'] if 'popular' in row else 0
            image = row['image'].strip() if isinstance(row['image'], str) else 'default_image.webp'

            existing = SpotifyStats.query.filter_by(
                orig_song_name=row['orig_song_name'], 
                song_name=row['song_name'], 
                artist=row['artist'], 
                total_streams=row['total_streams'], 
                popular=popular
            ).first()

            if not existing:
                spotify_stat = SpotifyStats(
                    artist=row['artist'],
                    image=image,
                    orig_song_name=row['orig_song_name'],
                    song_name=row['song_name'],
                    total_streams=row['total_streams'],
                    popular=popular,
                    date=data_as_of
                )
                db.session.add(spotify_stat)

        db.session.commit()
        print("Spotify stats data updated from Excel!")

        youtube_df = pd.read_excel(excel_file, sheet_name="youtubestats", dtype={'image': str})
        data_as_of = pd.read_excel(excel_file, sheet_name="youtubestats", header=None).iloc[0, 8]  # I1 is in row 0, column 8 (0-indexed)
       
        # Convert date format
        if isinstance(data_as_of, datetime):
            data_as_of = data_as_of.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(data_as_of, time):
            today = datetime.today()
            data_as_of = datetime.combine(today, data_as_of).strftime('%Y-%m-%d %H:%M:%S')
        else:
            data_as_of = datetime.strptime(data_as_of, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        # Insert into database
        for _, row in youtube_df.iterrows():
            popular = row['popular'] if 'popular' in row else 0
            image = row['image'].strip() if isinstance(row['image'], str) else 'default_image.webp'

            existing = YoutubeStats.query.filter_by(
                orig_song_name=row['orig_song_name'], 
                song_name=row['song_name'], 
                artist=row['artist'], 
                view_count=row['view_count'], 
                popular=popular
            ).first()

            if not existing:
                youtube_stat = YoutubeStats(
                    artist=row['artist'],
                    image=image,
                    orig_song_name=row['orig_song_name'],
                    song_name=row['song_name'],
                    view_count=row['view_count'],
                    popular=popular,
                    date=data_as_of
                )
                db.session.add(youtube_stat)

        db.session.commit()
        print("Youtube stats data updated from Excel!")

        shazam_df = pd.read_excel(excel_file, sheet_name="shazamstats", dtype={'image': str})
        data_as_of = pd.read_excel(excel_file, sheet_name="shazamstats", header=None).iloc[0, 8]  # I1 is in row 0, column 8 (0-indexed)
       
        # Convert date format
        if isinstance(data_as_of, datetime):
            data_as_of = data_as_of.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(data_as_of, time):
            today = datetime.today()
            data_as_of = datetime.combine(today, data_as_of).strftime('%Y-%m-%d %H:%M:%S')
        else:
            data_as_of = datetime.strptime(data_as_of, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

        # Insert into database
        for _, row in shazam_df.iterrows():
            popular = row['popular'] if 'popular' in row else 0
            image = row['image'].strip() if isinstance(row['image'], str) else 'default_image.webp'

            existing = ShazamStats.query.filter_by(
                orig_song_name=row['orig_song_name'], 
                song_name=row['song_name'], 
                artist=row['artist'], 
                shazam_count=row['shazam_count'], 
                popular=popular
            ).first()

            if not existing:
                shazam_stat = ShazamStats(
                    artist=row['artist'],
                    image=image,
                    orig_song_name=row['orig_song_name'],
                    song_name=row['song_name'],
                    shazam_count=row['shazam_count'],
                    popular=popular,
                    date=data_as_of
                )
                db.session.add(shazam_stat)

        db.session.commit()
        print("Shazam stats data updated from Excel!")

        fanbases_df = pd.read_excel(excel_file, sheet_name="Fanbase")
        for _, row in fanbases_df.iterrows():
            existing = Fanbase.query.filter_by(
                fb_name=row['fb_name'], 
                location=row['location']
            ).first()
            
            if not existing:
                fanbase = Fanbase(
                    logo=row['logo'],
                    fb_name=row['fb_name'],
                    location=row['location'],
                    focus=row['focus'],
                    description=row['description'],
                    x=row['x'],  
                    instagram=row['instagram'],
                    facebook=row['facebook'],
                    bluesky=row['bluesky'],
                    tiktok=row['tiktok'],
                    spotify=row['spotify'],
                    applemusic=row['applemusic']
                )
                db.session.add(fanbase)
        
        db.session.commit()
        print("Fanbases data updated from Excel!")

        projects_df = pd.read_excel(excel_file, sheet_name="Project")
        projects_df['date'] = projects_df['date'].dt.strftime('%Y-%m-%d')
        for _, row in projects_df.iterrows():
            existing = Project.query.filter_by(
                title=row['title'], 
                date=row['date']
            ).first()

            if not existing:
                project = Project(
                    title=row['title'],
                    date=row['date'],
                    location=row['location'],
                    image=row['image'], 
                    description=row['description'],
                    link=row['link']  
                )
                db.session.add(project)
        
        db.session.commit()
        print("Projects data updated from Excel!")
        
        events_df = pd.read_excel(excel_file, sheet_name='Event')
        events_df['date'] = pd.to_datetime(events_df['date'], errors='coerce')  # Convert the 'date' column to datetime
        events_df['date'] = events_df['date'].dt.strftime('%Y-%m-%d') 

        for _, row in events_df.iterrows():
            existing = Event.query.filter_by(
                date=row['date'], 
                title=row['title']
            ).first()
            
            if not existing:
                events = Event(
                    date=row['date'],
                    title=row['title'],
                    image=row['image'],
                    description=row['description'],
                    trending_tags=row['trending_tags'],
                    trending_position=row['trending_position'],
                    link=row['link']
                )
                db.session.add(events)

        db.session.commit()
        print("Event updated from Excel!")

        promotion_df = pd.read_excel(excel_file, sheet_name="Promotion")

        for _, row in promotion_df.iterrows():
            existing = Promotion.query.filter_by(brand_name=row['brand_name'], campaign_title=row['campaign_title']).first()

            if not existing:
                promotion = Promotion(
                    artist=row['artist'],
                    brand_name=row['brand_name'],
                    campaign_title=row['campaign_title'],
                    image_url=row['image_url'],
                    video_url=row['video_url'],
                    description=row['description'],
                    year=row['year']
                )
                db.session.add(promotion)

        db.session.commit()
        print("Promotion data updated from Excel!")
            
        # Clean Data - Fill NaNs with None
        banner_df = pd.read_excel(excel_file, sheet_name="Banner")
        banner_df = banner_df.where(pd.notna(banner_df), None) 

        for _, row in banner_df.iterrows():
            try:
                if not row['subpage'] or not row['title']:
                    print(f"Skipping row {_}: Missing subpage or title")
                    continue  

                banner = Banner(
                    subpage=str(row['subpage']).strip() if pd.notna(row['subpage']) else None,
                    title=str(row['title']).strip() if pd.notna(row['title']) else None,
                    link=str(row['link']).strip() if pd.notna(row['link']) else None,
                    date_added=pd.to_datetime(row['date_added']).date() if pd.notna(row['date_added']) else None
                )

                db.session.add(banner)
            
            except Exception as e:
                print(f"Error inserting row {_}: {e}")
        
        db.session.commit()
        print("Banner data inserted successfully!")

        product_df = pd.read_excel(excel_file, sheet_name='Product')
        for _, row in product_df.iterrows():
            existing = Product.query.filter_by(
                name=row['name'], 
                price=row['price'], 
                image=row['image']
            ).first()
            if not existing:
                product = Product(
                    name=row['name'],
                    price=row['price'],
                    image=row['image']
                )
                db.session.add(product)
        db.session.commit()
        print("Products updated from Excel!")

        fan_letters_df = pd.read_excel(excel_file, sheet_name='FanLetters')

        for _, row in fan_letters_df.iterrows():
            fanname = row['fanname'] if pd.notna(row['fanname']) else None
            image = row['image'] if pd.notna(row['image']) else None
            description = row['description'] if pd.notna(row['description']) else None

            if fanname or image:  # Ensure at least one field is provided
                existing = FanLetter.query.filter_by(fanname=fanname, image=image).first()
                if not existing:
                    fan_letter = FanLetter(fanname=fanname, image=image, description=description)
                    db.session.add(fan_letter)

        db.session.commit()
        print("Fan Letters updated from Excel!")

# Run the function to insert the data
insert_data_from_excel()
