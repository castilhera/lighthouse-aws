import json
import os
from tasks_db import TasksDatabase

def handler(event, context):
    task_id = event.get('pathParameters', {}).get('taskId')

    if not task_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "missing task id"})
        }

    try:
        db = TasksDatabase(table_name=os.environ['TASKS_TABLE'])
        task = db.get_task(task_id)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "internal server error "})
        }

    if not task:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "task not found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps(task)
    }
