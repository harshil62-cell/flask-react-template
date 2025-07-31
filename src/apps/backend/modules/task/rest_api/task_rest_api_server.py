from flask import Blueprint, request, jsonify
from modules.task.task_service import TaskService

task_blueprint = Blueprint("task", __name__, url_prefix="/tasks")

@task_blueprint.route("", methods=["GET"])
def get_tasks():
    return jsonify(TaskService.get_all_tasks()), 200

@task_blueprint.route("", methods=["POST"])
def create_task():
    data = request.get_json()
    task_id = TaskService.create_task(data)
    return jsonify({"_id": task_id}), 201

@task_blueprint.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    updated = TaskService.update_task(task_id, data)
    if updated:
        return jsonify({"message": "Task updated"}), 200
    return jsonify({"error": "Task not found"}), 404

@task_blueprint.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    deleted = TaskService.delete_task(task_id)
    if deleted:
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404

@task_blueprint.route("/<task_id>/comments", methods=["POST"])
def add_comment(task_id):
    comment = request.get_json()
    success = TaskService.add_comment(task_id, comment)
    if success:
        return jsonify({"message": "Comment added"}), 201
    return jsonify({"error": "Task not found"}), 404

@task_blueprint.route("/<task_id>/comments/<int:comment_id>", methods=["PUT"])
def update_comment(task_id, comment_id):
    comment_data = request.get_json()
    updated = TaskService.update_comment(task_id, comment_id, comment_data)
    if updated:
        return jsonify({"message": "Comment updated"}), 200
    return jsonify({"error": "Comment not found"}), 404

@task_blueprint.route("/<task_id>/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(task_id, comment_id):
    deleted = TaskService.delete_comment(task_id, comment_id)
    if deleted:
        return jsonify({"message": "Comment deleted"}), 200
    return jsonify({"error": "Comment not found"}), 404

