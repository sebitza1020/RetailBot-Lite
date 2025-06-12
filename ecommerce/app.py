from flask import Flask, render_template, redirect, url_for, session, request
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # In production, use a secure key from env

DB_PATH = Path(__file__).with_name('products.db')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image TEXT NOT NULL
        )"""
    )
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        sample_products = [
            ('Laptop', 1200.00, 'https://via.placeholder.com/150/0000FF/FFFFFF?text=Laptop'),
            ('Headphones', 199.99, 'https://via.placeholder.com/150/FF0000/FFFFFF?text=Headphones'),
            ('Smartphone', 899.50, 'https://via.placeholder.com/150/00FF00/FFFFFF?text=Phone'),
            ('Camera', 499.00, 'https://via.placeholder.com/150/FFFF00/000000?text=Camera'),
            ('Watch', 249.99, 'https://via.placeholder.com/150/FFA500/FFFFFF?text=Watch'),
            ('Tablet', 329.00, 'https://via.placeholder.com/150/800080/FFFFFF?text=Tablet')
        ]
        cur.executemany(
            "INSERT INTO products (name, price, image) VALUES (?, ?, ?)",
            sample_products,
        )
    conn.commit()
    conn.close()



def get_cart():
    return session.setdefault('cart', {})


def save_cart(cart):
    session['cart'] = cart


@app.route('/')
def index():
    init_db()
    cart = get_cart()
    cart_count = sum(cart.values())
    conn = get_db_connection()
    products = conn.execute(
        "SELECT id, name, price, image FROM products"
    ).fetchall()
    conn.close()
    return render_template('index.html', products=products, cart_count=cart_count)


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
    if cart:
        conn = get_db_connection()
        placeholders = ','.join('?' for _ in cart)
        query = f"SELECT id, name, price, image FROM products WHERE id IN ({placeholders})"
        products = {str(row['id']): row for row in conn.execute(query, tuple(cart.keys()))}
        conn.close()
        for pid, quantity in cart.items():
            product = products.get(pid)
            if product:
                item_total = product['price'] * quantity
                items.append({'product': product, 'quantity': quantity, 'total': item_total})
                total += item_total
    return render_template('cart.html', items=items, total=total)


@app.route('/clear', methods=['POST'])
def clear_cart():
    save_cart({})
    return redirect(url_for('view_cart'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
