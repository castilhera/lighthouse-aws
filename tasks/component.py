from aws_cdk import Stack
from constructs import Construct

from tasks.api.infrastructure import API
from tasks.database.infrastructure import Database


class Tasks(Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create dynamodb
        database = Database(self, "DB")

        # create api gateway and lambda endpoints
        api = API(self, "API", database.table.table_name)

        # grant access
        database.table.grant_write_data(api.create_task_lambda)
        database.table.grant_read_data(api.get_task_lambda)
        database.table.grant_read_write_data(api.update_task_lambda)
        database.table.grant_read_write_data(api.delete_task_lambda)
