from flask import Flask, render_template
import os

app = Flask(__name__)  # Initialize the Flask app

# Define the home page route
@app.route('/')
def home():
    return render_template('home.html')  # Render the home page

@app.route("/vibe")
def vibe():
    return render_template("vibe.html")

@app.route('/projects')
def projects():
    return render_template('projects.html')

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Use the environment variable for Render or default to 10000
    app.run(host='0.0.0.0', port=port)