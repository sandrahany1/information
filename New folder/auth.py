from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from app import mysql  

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (data['username'],))
    existing_user = cursor.fetchone()
    
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400
    
    cursor.execute("INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
                   (data['name'], data['username'], hashed_pw))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = %s", (data['username'],))
    user = cursor.fetchone()
    cursor.close()

    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user[1].encode('utf-8')):
        token = create_access_token(identity=str(user[0]))
        return jsonify({'token': token}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401


@auth_bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    current_user = get_jwt_identity()
    if str(current_user) != str(id):
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET name = %s, username = %s WHERE id = %s",
                   (data['name'], data['username'], id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User updated successfully'}), 200








