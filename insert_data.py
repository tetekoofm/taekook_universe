import pandas as pd
from models import db, Upcoming, Memory, Milestone, Product, Discography, MusicVideo
from app import app

def insert_data_from_excel():
    # Load the Excel file
    excel_file = 'taekook_universe.xlsx'

    with app.app_context():  # Ensure Flask app context is active

        # Read upcoming data from the upcoming sheet
        upcoming_df = pd.read_excel(excel_file, sheet_name='Upcoming')

        # Convert the 'date' column to string in YYYY-MM-DD format
        upcoming_df['date'] = upcoming_df['date'].dt.strftime('%Y-%m-%d')

        # Insert upcoming data into the upcoming table
        for _, row in upcoming_df.iterrows():
            # Check if the memory already exists
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


        # Read memory data from the memory sheet
        memory_df = pd.read_excel(excel_file, sheet_name='Memory')

        # Convert the 'date' column to string in YYYY-MM-DD format
        memory_df['date'] = memory_df['date'].dt.strftime('%Y-%m-%d')

        # Insert memory data into the memory table
        for _, row in memory_df.iterrows():
            # Check if the memory already exists
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

        # Read Milestones data from the milestones sheet
        milestone_df = pd.read_excel(excel_file, sheet_name='Milestone')

        # Convert the 'date' column to string in YYYY-MM-DD format
        milestone_df['date'] = milestone_df['date'].dt.strftime('%Y-%m-%d')

        # Insert Milestones data into the Milestones table
        for _, row in milestone_df.iterrows():
            # Check if the milestone already exists
            existing = Milestone.query.filter_by(
                date=row['date'], 
                artist=row['artist'], 
                title=row['title']
            ).first()
            if not existing:
                milestone = Milestone(
                    date=row['date'],
                    artist=row['artist'],
                    title=row['title'],
                    image=row['image'],
                    description=row['description']
                )
                db.session.add(milestone)
        db.session.commit()
        print("Milestones updated from Excel!")

        # Read Discography data from the second sheet
        discography_df = pd.read_excel(excel_file, sheet_name='Discography')
        for _, row in discography_df.iterrows():
            # Check if the discography entry already exists
            existing = Discography.query.filter_by(
                artist=row['artist'],
                album_name=row['album_name'],
                song_name=row['song_name']
            ).first()
            if not existing:
                duration_str = str(row['duration'])  # Converts time object or any other format to string
                discography = Discography(
                    artist=row['artist'],
                    album_name=row['album_name'],
                    song_name=row['song_name'],
                    release_date=row['release_date'],  # Ensure YYYY-MM-DD format
                    duration=duration_str
                )
                db.session.add(discography)
        db.session.commit()
        print("Discography updated from Excel!")

        # Read MusicVideos data from the third sheet
        music_video_df = pd.read_excel(excel_file, sheet_name='MusicVideo')
        for _, row in music_video_df.iterrows():
            # Check if the video already exists
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

        # Read Product data from the first sheet
        product_df = pd.read_excel(excel_file, sheet_name='Product')
        for _, row in product_df.iterrows():
            # Check if the product already exists
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

# Run the function to insert the data
insert_data_from_excel()
