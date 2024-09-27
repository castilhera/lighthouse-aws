import aws_cdk as cdk
import aws_cdk.aws_dynamodb as dynamodb
from constructs import Construct


class Database(Construct):
    def __init__(
            self,
            scope: Construct,
            id_: str
    ) -> None:
        super().__init__(scope, id_)

        self.table = dynamodb.Table(
            self,
            "TasksTable",
            partition_key=dynamodb.Attribute(
                name="taskId", type=dynamodb.AttributeType.STRING
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )
