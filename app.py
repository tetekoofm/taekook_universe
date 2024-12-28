from flask import Flask, render_template, request, redirect, session, url_for, jsonify
# from flask_sqlalchemy import SQLAlchemy
import os, secrets, random, calendar
from models import db, Upcoming, Memory, Milestone, Product, Discography, MusicVideo
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

# Home route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upcoming')
def upcoming():
    upcoming_events = Upcoming.query.order_by(Upcoming.date).all()
    # Convert date strings to datetime objects if necessary
    for event in upcoming_events:
        if isinstance(event.date, str):  # Check if date is a string
            event.date = datetime.strptime(event.date, '%Y-%m-%d')  # Adjust format as per your database
    return render_template("upcoming.html", upcoming=upcoming_events)

@app.route('/memories')
def memories():
    # Fetch all memories from the database
    memories_data = Memory.query.all()

    # Organize data by year and month using a defaultdict
    timeline_data = defaultdict(lambda: defaultdict(list))

    for memory in memories_data:
        year, month, day = map(int, memory.date.split('-'))  # Extract year, month, and day
        timeline_data[year][month].append({
            'id': memory.id,
            'title': memory.title,
            'date': f'{year}-{month:02}-{day:02}',  # Pass full date in YYYY-MM-DD format
            'image': memory.image,
            'description': memory.description,
        })

    # Ensure all months exist for each year
    for year in range(2013, 2025):  # Adjust year range as needed
        if year not in timeline_data:
            timeline_data[year] = {}
        for month in range(1, 13):  # Ensure each year has 12 months
            timeline_data[year].setdefault(month, [])

        # Sort months chronologically
        timeline_data[year] = {
            month: timeline_data[year][month]
            for month in sorted(timeline_data[year])
        }

    # Format years for display (e.g., '20' for 2020)
    formatted_years = {year: str(year)[-2:] for year in timeline_data.keys()}

    return render_template('memories.html', 
                           timeline_data=timeline_data, 
                           calendar=calendar, 
                           formatted_years=formatted_years)

@app.route('/get-event-details/<int:event_id>', methods=['GET'])
def get_event_details(event_id):
    # Fetch the memory by ID
    event = Memory.query.get(event_id)

    if event:
        # Return event details as JSON
        return jsonify({
            'title': event.title,
            'image': url_for('static', filename=f'images/{event.image}'),
            'description': event.description,
            'date': event.date
        })
    else:
        return jsonify({'error': 'Event not found'}), 404

@app.route('/milestones')
def milestones():
    # Query all milestones from the Milestone table, sorted by date in descending order
    milestones = Milestone.query.order_by(Milestone.date.desc()).all()

    # Pass the memories data to the template
    return render_template('milestones.html', milestones=milestones)

# Vibe route: Displays embedded songs and related content
@app.route('/vibe')
def vibe():
    # Fetch all the song names from the Discography table
    song_names = [song.song_name for song in Discography.query.all() if song.song_name]
    
    # Fetch all the music videos from the MusicVideos table
    music_video = MusicVideo.query.all()
    # Shuffle the list of videos to display them in a random order
    random.shuffle(music_video)

    # Debugging info
    if not song_names:
        print("No song names found.")
    if not music_video:
        print("No music videos found.")
    
    # Pass both song_names and music_videos to the template
    return render_template('vibe.html', song_names=song_names, music_videos=music_video)

# Store route: Displays products dynamically from the database
@app.route('/store')
def store():
    # Fetch all products from the Product table
    products = Product.query.all()
    
    # Optionally, you can set selected_quantities from session, etc.
    selected_quantities = {}  # You can fetch this from session or initialize as needed
    
    # Pass products and selected_quantities to the template
    return render_template('store.html', products=products, selected_quantities=selected_quantities)


# Add to Cart route: Adds selected items to the cart stored in the session
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = request.form['item']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])

    # Initialize cart in session if not present
    if 'cart' not in session:
        session['cart'] = {}

    # Update cart with the selected item and quantity
    if item in session['cart']:
        session['cart'][item]['quantity'] += quantity
    else:
        session['cart'][item] = {'quantity': quantity, 'price': price}

    session.modified = True  # Mark session as modified to save changes

    # Return a JSON response indicating success
    return jsonify({"message": "Item added to cart", "item": item, "quantity": quantity})

# Cart route: Displays the items in the user's cart
@app.route('/cart', methods=['POST', 'GET'])
def cart():
    cart_items = session.get('cart', {})
    
    # If there are no items in the cart, return a message
    if not cart_items:
        return render_template('cart.html', cart_items={}, total_price=0, message="Your cart is empty.")
    
    # Fetch all products from the database
    products = Product.query.all()
    
    # Handle POST request for updating the cart
    if request.method == 'POST':
        # Loop through each item and update the quantity based on user input
        for item in cart_items.keys():
            quantity = int(request.form.get(f"quantity_{item}", 0))
            if quantity > 0:
                cart_items[item]['quantity'] = quantity
            else:
                del cart_items[item]  # Remove item if quantity is 0

        session['cart'] = cart_items  # Update session with new cart items
        session.modified = True  # Mark session as modified to save changes
        return redirect('/cart')  # Redirect to cart to see updated items
    
    # Calculate the total price of items in the cart
    total_price = sum(item_details['quantity'] * item_details['price'] for item_details in cart_items.values())
    
    # Render the cart page with products and the calculated total price
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, products=products)


# Checkout route: Displays a summary of the cart and allows payment
@app.route('/checkout', methods=['POST', 'GET'])
def checkout():
    cart_items = session.get('cart', {})

    if not cart_items or all(item_details['quantity'] == 0 for item_details in cart_items.values()):
        return redirect('/cart')

    total_price = sum(item_details['quantity'] * item_details['price'] for item_details in cart_items.values())

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')

        if not name or not email or not address:
            return render_template('checkout.html', total_price=total_price, error="Please fill in all fields.")

        # Process order or save details here

        # Clear cart after order is processed
        session['cart'] = {}

        return render_template('thank_you.html', name=name, email=email, address=address, total_price=total_price)

    return render_template('checkout.html', total_price=total_price)


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
