from flask import Flask, render_template
import os

app = Flask(__name__)  # Initialize the Flask app

# Define the home page route
@app.route('/')
def home():
    return render_template('home.html')  # Render the home page

# Define the about page route
@app.route('/about')
def about():
    return render_template('about.html')  # Render the about page

@app.route('/projects')
def projects():
    return render_template('projects.html')

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))