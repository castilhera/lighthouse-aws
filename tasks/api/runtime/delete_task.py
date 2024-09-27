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
        db.delete_task(task_id)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "internal server error "})
        }

    return {
        "statusCode": 204,
        "body": ""
    }
