from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import secrets
from models import db, Product, Discography

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

# Vibe route: Displays embedded songs and related content
@app.route('/vibe')
def vibe():
    return render_template('vibe.html')  # Ensure the vibe.html template exists

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
    return redirect(url_for('store'))

# Cart route: Displays the items in the user's cart
@app.route('/cart', methods=['POST', 'GET'])
def cart():
    cart_items = session.get('cart', {})
    
    # If there are no items in the cart, return a message
    if not cart_items:
        return render_template('cart.html', cart_items={}, total_price=0, message="Your cart is empty.")
    
    # Fetch all products from the database
    products = Product.query.all()
    
    # Calculate the total price of items in the cart
    total_price = sum(item_details['quantity'] * item_details['price'] for item_details in cart_items.values())
    
    # Handle POST request for checkout (if any)
    if request.method == 'POST':
        return redirect('/checkout')
    
    # Render the cart page with products and the calculated total price
    return render_template('cart.html', cart_items=cart_items, total_price=total_price, products=products)


# Checkout route: Displays a summary of the cart and allows payment
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = session.get('cart', {})
    total_price = sum(item['quantity'] * item['price'] for item in cart_items.values())

    if request.method == 'POST':
        payment_method = request.form['payment_method']
        if payment_method == "paypal":
            return redirect(f"https://www.paypal.com/paypalme/tkfm9795/{total_price}")
        elif payment_method == "kofi":
            return redirect(f"https://ko-fi.com/tetekoofm?amount={total_price}&currency=USD")
        return "Invalid payment method.", 400  # Handle invalid payment methods

    return render_template('checkout.html', cart_items=cart_items, total_price=total_price)

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
