#!/usr/bin/env python3
import os
import aws_cdk as cdk
from tasks.component import Tasks

app = cdk.App()

Tasks(app,
      "Tasks",
    #   env=cdk.Environment(
    #       account=os.getenv('CDK_LH_AWS_ACCOUNT'),
    #       region=os.getenv('CDK_LH_AWS_REGION'))
    env=cdk.Environment(
        account="339712847288",
        region="us-west-2"),
)

app.synth()
