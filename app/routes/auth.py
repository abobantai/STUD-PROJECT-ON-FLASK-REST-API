from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

auth_bp = Blueprint('auth', __name__)

from app import models as model

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = model.User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401

    if check_password_hash(user.password, password):
        session_token = secrets.token_hex(16)
        model.Session.query.filter_by(user_id=user.id).delete()
        session = model.Session(user_id=user.id, session_token=session_token)
        model.db.session.add(session)
        model.db.session.commit()
        return jsonify({'message': 'Login successful', 'session_token': session_token}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Username, email, and password are required'}), 400

    if model.User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    if model.User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = model.User(username=username, email=email, password=hashed_password)
    
    model.db.session.add(new_user)
    model.db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201
@auth_bp.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    session_token = data.get('session_token')

    if not session_token:
        return jsonify({'error': 'Session token is required'}), 400

    session = model.Session.query.filter_by(session_token=session_token).first()

    if not session:
        return jsonify({'error': 'Invalid session token'}), 401

    model.db.session.delete(session)
    model.db.session.commit()

    return jsonify({'message': 'Logout successful'}), 200
    
    