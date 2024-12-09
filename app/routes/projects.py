from flask import Blueprint, jsonify, request
import csv
import os
from datetime import datetime

projects_bp = Blueprint('projects', __name__)

def read_projects_from_csv():
    projects = []
    csv_path = os.path.join(os.path.dirname(__file__), '../../data/projects.csv')
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                projects.append({
                    'id': row['id'],
                    'project_name': row['project_name'],
                    'description': row['description'],
                    'client_name': row['client_name'],
                    'country': row['country'],
                    'city': row['city'],
                    'business_category': row['business_category'],
                    'status': row['status'],
                    'start_date': row['start_date'],
                    'end_date': row['end_date'],
                    'created_at': row['created_at']
                })
        return projects
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []

@projects_bp.route('/api/projects', methods=['GET'])
def get_projects():
    projects = read_projects_from_csv()
    return jsonify(projects)

@projects_bp.route('/api/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    projects = read_projects_from_csv()
    project = next((project for project in projects if project['id'] == project_id), None)
    
    if project is None:
        return jsonify({'error': 'Project not found'}), 404
        
    return jsonify(project)

@projects_bp.route('/api/projects', methods=['POST'])
def create_project():
    try:
        new_project = request.get_json()
        projects = read_projects_from_csv()
        
        # 新しいIDを生成
        max_id = max([int(project['id']) for project in projects]) if projects else 0
        new_project['id'] = str(max_id + 1)
        
        # 作成日を設定
        new_project['created_at'] = datetime.now().strftime('%Y-%m-%d')
        
        # CSVファイルに追加
        csv_path = os.path.join(os.path.dirname(__file__), '../../data/projects.csv')
        fieldnames = ['id', 'project_name', 'description', 'client_name', 'country', 
                     'city', 'business_category', 'status', 'start_date', 'end_date', 'created_at']
        
        with open(csv_path, 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:  # ファイルが空の場合はヘッダーを書き込む
                writer.writeheader()
            writer.writerow(new_project)
        
        return jsonify(new_project), 201
        
    except Exception as e:
        print(f"Error creating project: {e}")
        return jsonify({'error': 'Failed to create project'}), 500

@projects_bp.route('/api/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    try:
        updated_data = request.get_json()
        csv_path = os.path.join(os.path.dirname(__file__), '../../data/projects.csv')
        
        # 現在のデータを読み込む
        projects = []
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            projects = list(reader)
        
        # 対象プロジェクトを更新
        project_updated = False
        for project in projects:
            if project['id'] == project_id:
                project.update(updated_data)
                project_updated = True
                break
        
        if not project_updated:
            return jsonify({'error': 'Project not found'}), 404
        
        # CSVファイルに書き戻す
        fieldnames = ['id', 'project_name', 'description', 'client_name', 'country', 
                     'city', 'business_category', 'status', 'start_date', 'end_date', 'created_at']
        with open(csv_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(projects)
        
        return jsonify({'message': 'Project updated successfully'})
        
    except Exception as e:
        print(f"Error updating project: {e}")
        return jsonify({'error': 'Failed to update project'}), 500 