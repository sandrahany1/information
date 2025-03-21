from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import mysql  

product_bp = Blueprint('product', __name__)


@product_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO products (pname, description, price, stock) VALUES (%s, %s, %s, %s)",
                   (data['pname'], data['description'], data['price'], data['stock']))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Product added successfully'}), 201


@product_bp.route('/products', methods=['GET'])
def get_products():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    product_list = []
    for product in products:
        product_list.append({
            'pid': product[0],
            'pname': product[1],
            'description': product[2],
            'price': product[3],
            'stock': product[4],
            'created_at': product[5].strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(product_list)


@product_bp.route('/products/<int:pid>', methods=['GET'])
def get_product(pid):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products WHERE pid = %s", (pid,))
    product = cursor.fetchone()
    cursor.close()
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify({
        'pid': product[0],
        'pname': product[1],
        'description': product[2],
        'price': product[3],
        'stock': product[4],
        'created_at': product[5].strftime('%Y-%m-%d %H:%M:%S')
    })


@product_bp.route('/products/<int:pid>', methods=['PUT'])
@jwt_required()
def update_product(pid):
    data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE products SET pname = %s, description = %s, price = %s, stock = %s WHERE pid = %s",
                   (data['pname'], data['description'], data['price'], data['stock'], pid))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Product updated successfully'}), 200


@product_bp.route('/products/<int:pid>', methods=['DELETE'])
@jwt_required()
def delete_product(pid):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM products WHERE pid = %s", (pid,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Product deleted successfully'}), 200





