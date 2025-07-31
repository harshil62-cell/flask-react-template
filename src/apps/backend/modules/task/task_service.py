from modules.db.mongo_client import db
from bson.objectid import ObjectId

tasks_collection = db.tasks

class TaskService:
    @staticmethod
    def create_task(data):
        result = tasks_collection.insert_one(data)
        return str(result.inserted_id)

    @staticmethod
    def get_all_tasks():
        return [{**task, "_id": str(task["_id"])} for task in tasks_collection.find()]

    @staticmethod
    def update_task(task_id, data):
        result = tasks_collection.update_one(
            {"_id": ObjectId(task_id)}, {"$set": data}
        )
        return result.modified_count

    @staticmethod
    def delete_task(task_id):
        result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count
    
    @staticmethod
    def add_comment(task_id, comment):
        task = tasks_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            return False
        comment["id"] = len(task.get("comments", [])) + 1
        tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$push": {"comments": comment}}
        )
        return True

    @staticmethod
    def update_comment(task_id, comment_id, new_data):
        result = tasks_collection.update_one(
            {"_id": ObjectId(task_id), "comments.id": comment_id},
            {"$set": {"comments.$.text": new_data.get("text", ""),
                      "comments.$.author": new_data.get("author", "")}}
        )
        return result.modified_count > 0

    @staticmethod
    def delete_comment(task_id, comment_id):
        result = tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$pull": {"comments": {"id": comment_id}}}
        )
        return result.modified_count > 0
