from flask import Blueprint, request, jsonify
from database import Session
from Task import Task
from middleware import token_required

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
@token_required
def get_tasks(current_user):
    session = Session()
    
    if current_user['role'] == 'admin':
        print(f"Admin User {current_user['id']} fetching ALL tasks")
        tasks = session.query(Task).all()
    else:
        print(f"Standard User {current_user['id']} fetching OWN tasks")
        tasks = session.query(Task).filter_by(owner_id=current_user['id']).all()
    
    output = []
    for task in tasks:
        output.append({
            'id': task.id, 
            'title': task.title, 
            'owner_id': task.owner_id
        })
    
    session.close()
    return jsonify({'tasks': output})

@tasks_bp.route('/tasks', methods=['POST'])
@token_required
def create_task(current_user):
    data = request.get_json()
    session = Session()
    
    new_task = Task(title=data['title'], owner_id=current_user['id'])
    session.add(new_task)
    session.commit()
    session.close()
    
    return jsonify({'message': 'Task created!'}), 201

@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(current_user, task_id):
    session = Session()
    task = session.query(Task).filter_by(id=task_id).first()
    
    if not task:
        session.close()
        return jsonify({'message': 'Task not found'}), 404

    if current_user['role'] != 'admin' and task.owner_id != current_user['id']:
        session.close()
        return jsonify({'message': 'Permission denied'}), 403

    session.delete(task)
    session.commit()
    session.close()
    
    return jsonify({'message': 'Task deleted'}), 200