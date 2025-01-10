import pandas as pd
from models import db, Upcoming, Memory, Milestone, Product, Discography, MusicVideo, Fanbase, Project
from app import app

def insert_data_from_excel():
    excel_file = 'taekook_universe.xlsx'

    with app.app_context():

        upcoming_df = pd.read_excel(excel_file, sheet_name='Upcoming')
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

        memory_df = pd.read_excel(excel_file, sheet_name='Memory')
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

        milestone_df = pd.read_excel(excel_file, sheet_name='Milestone')
        milestone_df['date'] = milestone_df['date'].dt.strftime('%Y-%m-%d')
        for _, row in milestone_df.iterrows():
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

        discography_df = pd.read_excel(excel_file, sheet_name='Discography')
        for _, row in discography_df.iterrows():
            existing = Discography.query.filter_by(
                artist=row['artist'],
                album_name=row['album_name'],
                song_name=row['song_name']
            ).first()
            if not existing:
                duration_str = str(row['duration'])
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
                    description=row['description']
                )
                db.session.add(fanbase)
        
        db.session.commit()
        print("Fanbases data updated from Excel!")

        projects_df = pd.read_excel(excel_file, sheet_name="Project")
        projects_df['date'] = projects_df['date'].dt.strftime('%Y-%m-%d')
        for _, row in projects_df.iterrows():
            # Check if the project already exists (based on title or another unique field)
            existing = Project.query.filter_by(
                title=row['title'],  # Assuming title is unique
                date=row['date']
            ).first()

            if not existing:
                project = Project(
                    title=row['title'],
                    date=row['date'],
                    location=row['location'],
                    image=row['image'], 
                    description=row['description'],
                    link=row['link']  # Assuming there's a 'link' column in your Excel sheet
                )
                db.session.add(project)
        
        db.session.commit()
        print("Projects data updated from Excel!")
        
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

# Run the function to insert the data
insert_data_from_excel()
