import boto3
import uuid

class TasksDatabase():

    _dynamodb = boto3.resource("dynamodb")

    def __init__(self, table_name: str):
        self._table = self._dynamodb.Table(table_name)


    def create_task(self, title: str, description: str, status: str):
        task = {
            'taskId': str(uuid.uuid4()),
            'title': title,
            'description': description,
            'status': status
        }

        self._table.put_item(Item=task)

        return task


    def update_task(self, task_id: str, title: str, description: str, status: str):
        update_expression = "set #title = :t, #description = :d, #status = :s"
        expression_attribute_values = {
            ':t': title,
            ':d': description,
            ':s': status
        }

        expression_attribute_names = {
            '#title': 'title',
            '#description': 'description',
            '#status': 'status'
        }

        self._table.update_item(
            Key={'taskId': task_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names
        )


    def get_task(self, task_id: str):
        response = self._table.get_item(Key={"taskId": task_id})
        return response["Item"] if "Item" in response else None


    def delete_task(self, task_id: str) -> None:
        self._table.delete_item(Key={"taskId": task_id})
