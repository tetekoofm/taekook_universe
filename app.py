from flask import Flask, render_template, request, redirect, session, url_for
import os
import secrets


app = Flask(__name__)  # Initialize the Flask app

# Set a secret key for session management
app.secret_key = secrets.token_hex(16)  # Generate a random secret key for the session


# Define the home page route
@app.route('/')
def home():
    return render_template('home.html')  # Render the home page

@app.route("/vibe")
def vibe():
    return render_template("vibe.html")

@app.route('/store')
def store():
    # Retrieve selected quantities from the session or initialize as empty
    selected_quantities = session.get('selected_quantities', {})
    return render_template('store.html', selected_quantities=selected_quantities)

@app.route('/order', methods=['POST'])
def order():
    item = request.form['item']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    
    total_amount = price * quantity
    
    # Pass the total_amount to the order page
    return render_template('order.html', item=item, quantity=quantity, total_amount=total_amount)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = request.form['item']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    
    # Save selected quantity in session
    if 'selected_quantities' not in session:
        session['selected_quantities'] = {}
    session['selected_quantities'][item] = quantity

    # Initialize cart if it's not already in the session
    if 'cart' not in session:
        session['cart'] = {}

    # Add the item to the cart or update the quantity
    if item in session['cart']:
        session['cart'][item]['quantity'] += quantity  # Add quantity
    else:
        session['cart'][item] = {'quantity': quantity, 'price': price}  # Add new item with price and quantity

    session.modified = True  # Ensure session is updated
    return redirect(url_for('store'))  # Redirect back to the store page

@app.route('/cart', methods=['POST', 'GET'])
def cart():
    cart_items = session.get('cart', {})
    if not cart_items:
        return render_template('cart.html', cart_items={}, total_price=0, message="Your cart is empty.")
    
    total_price = sum(item_details['quantity'] * item_details['price'] for item_details in cart_items.values())
    if request.method == 'POST':
        return redirect('/checkout')
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Retrieve cart items from the session
    cart_items = session.get('cart', {})
    
    # Calculate the total price
    total_price = sum(item_details['quantity'] * item_details['price'] for item_details in cart_items.values())
    
    if request.method == 'POST':
        # Process the payment or redirect to the payment gateway
        # You can perform logic here, like handling payment or redirecting to PayPal/Ko-Fi
        return redirect('/payment')  # Replace with actual payment route
    
    # Display checkout page (a form to confirm details or payment)
    return render_template('checkout.html', cart_items=cart_items, total_price=total_price)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    total_price = float(request.form['total_price'])  # Get the total price from the form
    payment_method = request.form['payment_method']    # Get the selected payment method (PayPal or Ko-fi)
    
    if payment_method == "paypal":
        # Redirect to PayPal with the total amount
        paypal_url = f"https://www.paypal.com/paypalme/tkfm9795/{total_price}"
        return redirect(paypal_url)
    elif payment_method == "kofi":
        # Redirect to Ko-fi with the total amount
        kofi_url = f"https://ko-fi.com/tetekoofm?amount={total_price}&currency=USD"
        return redirect(kofi_url)
    
    # If no valid payment method was selected
    return "Invalid payment method.", 400

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Use the environment variable for Render or default to 10000
    app.run(debug=True, host='0.0.0.0', port=port)