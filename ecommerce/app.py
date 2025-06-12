from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # In production, use a secure key from env

# Example product catalog
PRODUCTS = [
    {'id': 1, 'name': 'Laptop', 'price': 1200.00, 'image': 'https://via.placeholder.com/150'},
    {'id': 2, 'name': 'Headphones', 'price': 199.99, 'image': 'https://via.placeholder.com/150'},
    {'id': 3, 'name': 'Smartphone', 'price': 899.50, 'image': 'https://via.placeholder.com/150'},
]


def get_cart():
    return session.setdefault('cart', {})


def save_cart(cart):
    session['cart'] = cart


@app.route('/')
def index():
    cart = get_cart()
    cart_count = sum(cart.values())
    return render_template('index.html', products=PRODUCTS, cart_count=cart_count)


@app.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart = get_cart()
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    save_cart(cart)
    return redirect(url_for('index'))


@app.route('/cart')
def view_cart():
    cart = get_cart()
    items = []
    total = 0
    for product in PRODUCTS:
        pid = str(product['id'])
        quantity = cart.get(pid, 0)
        if quantity:
            item_total = product['price'] * quantity
            items.append({'product': product, 'quantity': quantity, 'total': item_total})
            total += item_total
    return render_template('cart.html', items=items, total=total)


@app.route('/clear', methods=['POST'])
def clear_cart():
    save_cart({})
    return redirect(url_for('view_cart'))


if __name__ == '__main__':
    app.run(debug=True)
