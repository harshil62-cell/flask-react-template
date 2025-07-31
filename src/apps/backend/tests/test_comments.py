import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
import pytest
import mongomock
from flask import Flask
from src.apps.backend.server import app as flask_app
from modules.task.db.task_repo import TaskRepo
from modules.comment.db.comment_repo import CommentRepo

@pytest.fixture(autouse=True)
def mock_mongo(monkeypatch):
    # Use mongomock's MongoClient instead of pymongo's
    mock_client = mongomock.MongoClient()
    mock_db = mock_client["test_db"]

    monkeypatch.setattr(TaskRepo, "collection", mock_db["tasks"])
    monkeypatch.setattr(CommentRepo, "collection", mock_db["comments"])

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def task_id():
    result = TaskRepo.collection.insert_one({
        "title": "Test Task",
        "description": "Test Description",
        "comments": []
    })
    return str(result.inserted_id)

@pytest.fixture
def created_comment(client, task_id):
    response = client.post(f"/api/tasks/{task_id}/comments", json={
        "author": "Harshil",
        "text": "Original Comment"
    })
    return response.json.get("comment_id") or response.json.get("_id")

def test_create_comment(client, task_id):
    response = client.post(f"/api/tasks/{task_id}/comments", json={
        "author": "Harshil",
        "text": "Test comment"
    })
    assert response.status_code == 201
    assert "comment_id" in response.json or "_id" in response.json

def test_get_comments(client, task_id):
    response = client.get(f"/api/tasks/{task_id}/comments")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_update_comment(client, task_id, created_comment):
    response = client.put(f"/api/tasks/{task_id}/comments/{created_comment}", json={
        "text": "Updated comment text"
    })
    assert response.status_code == 200
    assert response.json.get("message") == "Comment updated"

def test_delete_comment(client, task_id, created_comment):
    response = client.delete(f"/api/tasks/{task_id}/comments/{created_comment}")
    assert response.status_code == 200
    assert response.json.get("message") == "Comment deleted"
