from flask import Blueprint, jsonify, request
import csv
import os
import traceback
import logging

# ロギングの設定
logger = logging.getLogger(__name__)

users_bp = Blueprint('users', __name__)

def read_users_from_csv():
    users = []
    csv_path = os.path.join(os.path.dirname(__file__), '../../data/users.csv')
    
    try:
        logger.info(f"Attempting to read CSV from: {csv_path}")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Directory contents of data folder:")
        data_dir = os.path.dirname(csv_path)
        if os.path.exists(data_dir):
            logger.info(f"Files in data directory: {os.listdir(data_dir)}")
        else:
            logger.error(f"Data directory does not exist: {data_dir}")
            
        logger.info(f"File exists: {os.path.exists(csv_path)}")
        
        if not os.path.exists(csv_path):
            alternative_path = os.path.join(os.getcwd(), 'data', 'users.csv')
            logger.info(f"Trying alternative path: {alternative_path}")
            if os.path.exists(alternative_path):
                csv_path = alternative_path
                logger.info("Using alternative path")
            else:
                logger.error("Alternative path also not found")
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append({
                    'id': row['id'],
                    'email': row['email'],
                    'name': row['name'],
                    'prefecture': row['prefecture']
                })
            logger.info(f"Successfully read {len(users)} users from CSV")
        return users
    except Exception as e:
        logger.error(f"Error reading CSV: {str(e)}")
        logger.error("Full traceback:")
        logger.error(traceback.format_exc())
        return []

@users_bp.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = read_users_from_csv()
        logger.info(f"Returning {len(users)} users")
        return jsonify(users)
    except Exception as e:
        logger.error(f"Error in get_users: {str(e)}")
        return jsonify({'error': str(e)}), 500

@users_bp.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        users = read_users_from_csv()
        user = next((user for user in users if user['id'] == user_id), None)
        
        if user is None:
            logger.warning(f"User not found: {user_id}")
            return jsonify({'error': 'User not found'}), 404
            
        logger.info(f"Returning user: {user_id}")
        return jsonify(user)
    except Exception as e:
        logger.error(f"Error in get_user: {str(e)}")
        return jsonify({'error': str(e)}), 500

@users_bp.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        updated_data = request.get_json()
        logger.info(f"Updating user {user_id} with data: {updated_data}")
        
        csv_path = os.path.join(os.path.dirname(__file__), '../../data/users.csv')
        
        if not os.path.exists(csv_path):
            alternative_path = os.path.join(os.getcwd(), 'data', 'users.csv')
            if os.path.exists(alternative_path):
                csv_path = alternative_path
                logger.info("Using alternative path for update")
            else:
                logger.error("CSV file not found for update")
                return jsonify({'error': 'CSV file not found'}), 500
        
        users = []
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            users = list(reader)
        
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
            logger.warning(f"User not found for update: {user_id}")
            return jsonify({'error': 'User not found'}), 404
        
        fieldnames = ['id', 'email', 'name', 'prefecture']
        with open(csv_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)
        
        logger.info(f"Successfully updated user: {user_id}")
        return jsonify({'message': 'User updated successfully'})
        
    except Exception as e:
        logger.error(f"Error updating user: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'Failed to update user: {str(e)}'}), 500