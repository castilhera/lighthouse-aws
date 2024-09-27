import json
import os
from tasks_db import TasksDatabase

def handler(event, context):
    body = json.loads(event['body'])

    title = body.get('title')

    if not title:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid title"})
        }

    description = body.get('description')

    if not description:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid description"})
        }

    status = body.get('status')

    if status not in ['pending', 'in-progress', 'completed']:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid status"})
        }

    try:
        db = TasksDatabase(table_name=os.environ['TASKS_TABLE'])
        task = db.create_task(title, description, status)
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "internal server error "})
        }

    return {
        "statusCode": 201,
        "body": json.dumps(task)
    }
