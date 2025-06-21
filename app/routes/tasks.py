from flask import Blueprint, request, jsonify
from app import models as model

tasks_bp = Blueprint('tasks', __name__)

def get_user_id_from_token(token):
    session_obj = model.Session.query.filter_by(session_token=token).first()
    if not session_obj:
        return None
    return session_obj.user_id

@tasks_bp.route('/tasks', methods=['POST'])
def get_tasks():
    data = request.get_json()
    token = data.get("token")
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid session token'}), 401

    tasks = model.Task.query.filter_by(user_id=user_id).all()
    tasks_list = [{'id': task.id, 'title': task.title, 'description': task.description, 'status': task.status} for task in tasks]
    return jsonify({'tasks': tasks_list}), 200

@tasks_bp.route('/create-tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    token = data.get("token")
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid session token'}), 401

    title = data.get('title')
    description = data.get('description', '')
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    new_task = model.Task(title=title, description=description, user_id=user_id)
    model.db.session.add(new_task)
    model.db.session.commit()

    return jsonify({'message': 'Task created successfully', 'task_id': new_task.id}), 201

@tasks_bp.route('/update-task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    token = data.get("token")
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid session token'}), 401

    task = model.Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    model.db.session.commit()

    return jsonify({'message': 'Task updated successfully'}), 200

@tasks_bp.route('/delete-task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    data = request.get_json()
    token = data.get("token")
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid session token'}), 401

    task = model.Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    model.db.session.delete(task)
    model.db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

@tasks_bp.route('/complete-task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    data = request.get_json()
    token = data.get("token")
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid session token'}), 401

    task = model.Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    if task.status == "new":
        task.status = "in-progress"
    elif task.status == "in-progress":
        task.status = "completed"
    elif task.status == "completed":
        return jsonify({'message': 'Already completed'}), 400

    model.db.session.commit()
    return jsonify({'message': f'Task status changed to {task.status}'}), 200

@tasks_bp.route('/uncomplete-task/<int:task_id>', methods=['POST'])
def uncomplete_task(task_id):
    data = request.get_json()
    token = data.get("token")
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid session token'}), 401

    task = model.Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    if task.status == "completed":
        task.status = "in-progress"
    elif task.status == "in-progress":
        return jsonify({'message': 'Already in progress'}), 400
    elif task.status == "new":
        return jsonify({'message': 'Already new'}), 400

    model.db.session.commit()
    return jsonify({'message': f'Task status changed to {task.status}'}), 200
@tasks_bp.route('/task/<int:task_id>', methods=['POST'])
def get_task(task_id):
    data = request.get_json()
    token = data.get("token")
    user_id = get_user_id_from_token(token)
    if not user_id:
        return jsonify({'error': 'Invalid session token'}), 401

    task = model.Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    task_data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status
    }
    return jsonify({'task': task_data}), 200