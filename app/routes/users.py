from flask import Blueprint, jsonify
import csv
import os

users_bp = Blueprint('users', __name__)

def read_users_from_csv():
    users = []
    csv_path = os.path.join(os.path.dirname(__file__), '../../data/users.csv')
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append({
                    'id': row['id'],
                    'email': row['email'],
                    'name': row['name'],
                    'prefecture': row['prefecture']
                })
        return users
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

@users_bp.route('/api/users', methods=['GET'])
def get_users():
    users = read_users_from_csv()
    return jsonify(users)

@users_bp.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    users = read_users_from_csv()
    user = next((user for user in users if user['id'] == user_id), None)
    
    if user is None:
        return jsonify({'error': 'User not found'}), 404
        
    return jsonify(user)