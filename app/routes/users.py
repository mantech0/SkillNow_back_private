from flask import Blueprint, jsonify, request
import csv
import os
import traceback

users_bp = Blueprint('users', __name__)

def read_users_from_csv():
    users = []
    csv_path = os.path.join(os.path.dirname(__file__), '../../data/users.csv')
    
    try:
        print(f"Attempting to read CSV from: {csv_path}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Directory contents: {os.listdir(os.path.dirname(csv_path))}")
        print(f"File exists: {os.path.exists(csv_path)}")
        
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
        print(f"Error reading CSV: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
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

@users_bp.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        # リクエストボディからデータを取得
        updated_data = request.get_json()
        
        # CSVファイルのパス
        csv_path = os.path.join(os.path.dirname(__file__), '../../data/users.csv')
        
        # 現在のデータを読み込む
        users = []
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            users = list(reader)
        
        # 対象ユーザーを更新
        user_updated = False
        for user in users:
            if user['id'] == user_id:
                user.update({
                    'email': updated_data.get('email', user['email']),
                    'name': updated_data.get('name', user['name']),
                    'prefecture': updated_data.get('prefecture', user['prefecture'])
                })
                user_updated = True
                break
        
        if not user_updated:
            return jsonify({'error': 'User not found'}), 404
        
        # CSVファイルに書き戻す
        fieldnames = ['id', 'email', 'name', 'prefecture']
        with open(csv_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)
        
        return jsonify({'message': 'User updated successfully'})
        
    except Exception as e:
        print(f"Error updating user: {e}")
        return jsonify({'error': 'Failed to update user'}), 500