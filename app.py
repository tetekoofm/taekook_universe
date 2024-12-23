from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
import os, secrets, random
from models import db, Memory, Milestone, Product, Discography, MusicVideo

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

@app.route('/memories')
def memories():
    # Query all memories from the Memory table, sorted by date in descending order
    memories = Memory.query.order_by(Memory.date.desc()).all()

    # Pass the memories data to the template
    return render_template('memories.html', memories=memories)

# @app.route('/milestone')
# def milestone():
#     # Fetch milestones from the database, ordered by date descending
#     milestones = Milestone.query.order_by(Milestone.date.desc()).all()
#     return render_template('milestone.html', milestones=milestones)

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
