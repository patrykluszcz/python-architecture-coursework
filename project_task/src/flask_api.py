import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask, jsonify, request, render_template, send_file
from flask_cors import CORS
from product import Product
from user import User
from cart import Cart
from order import Order, OrderStatus
from ecommerce import ECommercePlatform

parent_dir = Path(__file__).parent.parent

app = Flask(__name__, 
            template_folder=str(parent_dir / 'templates'), 
            static_folder=str(parent_dir / 'static'))
CORS(app)

platform = ECommercePlatform()

demo_products = [
    Product("P001", "Laptop", 999.99, 10),
    Product("P002", "Mysz", 29.99, 50),
    Product("P003", "Klawiatura", 99.99, 30),
    Product("P004", "Monitor", 299.99, 15),
    Product("P005", "Headphones", 149.99, 20),
]

demo_users = [
    User("U001", "john_doe", "john@example.com"),
    User("U002", "anna_nowak", "anna@example.com"),
    User("U003", "bob_smith", "bob@example.com"),
]

for product in demo_products:
    platform.register_product(product)

for user in demo_users:
    user.set_address("Sample Address")
    platform.register_user(user)

data_dir = parent_dir / 'data'

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/api/products", methods=["GET"])
def get_products():
    try:
        products = platform.get_all_products()
        return jsonify({
            'products': [
                {
                    'product_id': p.product_id,
                    'name': p.name,
                    'price': p.price,
                    'stock': p.stock
                }
                for p in products
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/products/<product_id>", methods=["GET"])
def get_product(product_id):
    try:
        product = platform.get_product(product_id)
        if not product:
            return jsonify({'error': 'Produkt nie znaleziony'}), 404
        return jsonify({
            'product': {
                'product_id': product.product_id,
                'name': product.name,
                'price': product.price,
                'stock': product.stock
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/products", methods=["POST"])
def create_product():
    try:
        data = request.get_json()
        product = Product(
            data['product_id'],
            data['name'],
            float(data['price']),
            int(data['stock'])
        )
        platform.register_product(product)
        return jsonify({
            'message': 'Produkt dodany',
            'product': {
                'product_id': product.product_id,
                'name': product.name,
                'price': product.price,
                'stock': product.stock
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        users = platform._users
        return jsonify({
            'users': [
                {
                    'user_id': u.user_id,
                    'username': u.username,
                    'email': u.email,
                    'address': u.address
                }
                for u in users.values()
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = platform.get_user(user_id)
        if not user:
            return jsonify({'error': 'Użytkownik nie znaleziony'}), 404
        return jsonify({
            'user': {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'address': user.address
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        user = User(
            data['user_id'],
            data['username'],
            data['email']
        )
        if data.get('address'):
            user.set_address(data['address'])
        platform.register_user(user)
        return jsonify({
            'message': 'Użytkownik utworzony',
            'user': {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'address': user.address
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/users/<user_id>/address", methods=["POST"])
def update_user_address(user_id):
    try:
        user = platform.get_user(user_id)
        if not user:
            return jsonify({'error': 'Użytkownik nie znaleziony'}), 404
        
        data = request.get_json()
        user.set_address(data['address'])
        
        return jsonify({
            'message': 'Adres zaktualizowany',
            'user': {
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'address': user.address
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/cart/<user_id>", methods=["GET"])
def get_cart(user_id):
    try:
        cart = platform.get_cart(user_id)
        if not cart:
            return jsonify({'error': 'Użytkownik nie znaleziony'}), 404
        
        items = cart.get_items()
        return jsonify({
            'items': [
                {
                    'product_id': product.product_id,
                    'name': product.name,
                    'price': product.price,
                    'quantity': quantity
                }
                for product, quantity in items
            ],
            'total': cart.get_total_price()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/cart/<user_id>/add", methods=["POST"])
def add_to_cart(user_id):
    try:
        data = request.get_json()
        result = platform.add_to_cart(
            user_id,
            data['product_id'],
            data['quantity']
        )
        if not result:
            return jsonify({'error': 'Nie można dodać do koszyka'}), 400
        return jsonify({'message': 'Produkt dodany do koszyka'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/cart/<user_id>/remove", methods=["DELETE"])
def remove_from_cart(user_id):
    try:
        data = request.get_json()
        platform.remove_from_cart(user_id, data['product_id'])
        return jsonify({'message': 'Produkt usunięty z koszyka'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/orders", methods=["POST"])
def create_order():
    try:
        data = request.get_json()
        order = platform.checkout(data['user_id'])
        if not order:
            return jsonify({'error': 'Nie można utworzyć zamówienia. Sprawdź czy koszyk nie jest pusty i czy użytkownik ma ustawiony adres.'}), 400
        return jsonify({
            'message': 'Zamówienie złożone',
            'order': {
                'order_id': order.order_id,
                'user_id': order.user.user_id,
                'status': order.status.value,
                'total_price': order.total_price,
                'creation_date': order.creation_date.isoformat(),
                'items': [
                    {
                        'product_id': product.product_id,
                        'name': product.name,
                        'price': product.price,
                        'quantity': quantity
                    }
                    for product, quantity in order.items
                ]
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/orders/<order_id>", methods=["GET"])
def get_order(order_id):
    try:
        order = platform.get_order(order_id)
        if not order:
            return jsonify({'error': 'Zamówienie nie znaleziono'}), 404
        
        return jsonify({
            'order': {
                'order_id': order.order_id,
                'user_id': order.user.user_id,
                'status': order.status.value,
                'total_price': order.total_price,
                'creation_date': order.creation_date.isoformat(),
                'items': [
                    {
                        'product_id': product.product_id,
                        'name': product.name,
                        'price': product.price,
                        'quantity': quantity
                    }
                    for product, quantity in order.items
                ]
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/orders/<order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    try:
        data = request.get_json()
        order = platform.get_order(order_id)
        
        if not order:
            return jsonify({'error': 'Zamówienie nie znaleziono'}), 404
        
        status_map = {
            'pending': OrderStatus.PENDING,
            'confirmed': OrderStatus.CONFIRMED,
            'shipped': OrderStatus.SHIPPED,
            'delivered': OrderStatus.DELIVERED,
            'cancelled': OrderStatus.CANCELLED
        }
        
        new_status = status_map.get(data['status'].lower())
        if not new_status:
            return jsonify({'error': 'Nieprawidłowy status'}), 400
        
        platform.update_order_status(order_id, new_status)
        return jsonify({'message': 'Status zamówienia zaktualizowany'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/orders/<order_id>/xml", methods=["GET"])
def download_order_xml(order_id):
    try:
        order = platform.get_order(order_id)
        if not order:
            return jsonify({'error': 'Zamówienie nie znaleziono'}), 404
        
        xml_content = order.to_xml()
        
        # Save to file
        file_path = data_dir / f'{order_id}.xml'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        return send_file(
            file_path,
            mimetype='application/xml',
            as_attachment=True,
            download_name=f'{order_id}.xml'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/api/users/<user_id>/orders", methods=["GET"])
def get_user_orders(user_id):
    try:
        user = platform.get_user(user_id)
        if not user:
            return jsonify({'error': 'Użytkownik nie znaleziony'}), 404
        
        orders = platform.get_user_orders(user_id)
        return jsonify({
            'orders': [
                {
                    'order_id': o.order_id,
                    'user_id': o.user.user_id,
                    'status': o.status.value,
                    'total_price': o.total_price,
                    'creation_date': o.creation_date.isoformat(),
                    'items': [
                        {
                            'product_id': product.product_id,
                            'name': product.name,
                            'price': product.price,
                            'quantity': quantity
                        }
                        for product, quantity in o.items
                    ]
                }
                for o in orders
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5004)
