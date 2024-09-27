import os
from aws_cdk import (
    aws_lambda,
    aws_apigateway
)
from constructs import Construct


class API(Construct):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            table_name: str,
            **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        code_path = os.path.join(os.getcwd(), 'tasks', 'api', 'runtime')
        code = aws_lambda.Code.from_asset(path=code_path)

        def _create_lambda(lambda_name: str, handler_name: str):
            return aws_lambda.Function(
                self, lambda_name,
                runtime=aws_lambda.Runtime.PYTHON_3_12,
                handler=f"{handler_name}.handler",
                code=code,
                environment={
                    "TASKS_TABLE": table_name
                }
            )

        self.create_task_lambda = _create_lambda("CreateTaskFunction", "create_task")
        self.get_task_lambda = _create_lambda("GetTaskFunction", "get_task")
        self.update_task_lambda = _create_lambda("UpdateTaskFunction", "update_task")
        self.delete_task_lambda = _create_lambda("DeleteTaskFunction", "delete_task")

        self.api = aws_apigateway.RestApi(
            self,
            "TasksAPI",
            rest_api_name="Tasks Service"
        )

        tasks = self.api.root.add_resource("tasks")
        # create
        tasks.add_method("POST", aws_apigateway.LambdaIntegration(self.create_task_lambda))

        task = tasks.add_resource("{taskId}")
        #read
        task.add_method("GET", aws_apigateway.LambdaIntegration(self.get_task_lambda))
        #update
        task.add_method("PUT", aws_apigateway.LambdaIntegration(self.update_task_lambda))
        # delete
        task.add_method("DELETE", aws_apigateway.LambdaIntegration(self.delete_task_lambda))
