# create_table.py
from app import app
from models import db
import os

# Set the database URI to use taekook.db
project_dir = os.path.abspath(os.path.dirname(__file__))
db_file = os.path.join(project_dir, 'instance', 'taekook.db')

# Create all tables in taekook.db
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file}"

# Create the tables
with app.app_context():
    db.drop_all()
    print("Tables dropped successfully in taekook.db!")
    db.create_all()
    print("Tables created successfully in taekook.db!")
