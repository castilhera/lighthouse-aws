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

    body = json.loads(event['body'])

    title = body.get('title')

    if not title:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "invalid title"})
        }

    description = body.get('description')

    if not description:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "invalid description"})
        }

    status = body.get('status')

    if status not in ['pending', 'in-progress', 'completed']:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "invalid status"})
        }

    try:
        db = TasksDatabase(table_name=os.environ['TASKS_TABLE'])
        db.update_task(task_id, title, description, status)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "internal server error "})
        }

    return {
        "statusCode": 204,
        "body": ""
    }
