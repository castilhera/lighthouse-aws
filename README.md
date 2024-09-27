# lighthouse-aws

This is a Task App, a serverless CRUD API, developed using AWS CDK and Python to deploy on AWS using API Gateway, AWS Lambda and DynamoDB.

## Setup

### Create the venv

First, create a virtualenv:

- on MacOS and Linux:

```
$ python -m venv .venv
```

- on Windows

```
% .venv\Scripts\activate.bat
```

Then, activate your virtualenv.

- on MacOS and Linux:
```
$ source .venv/bin/activate
```

- on Windows

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

### Configure AWS credentials

Check if you have AWS credentials configured.

If so, next step is setup your environment variables in the `app.py` file:
* CDK_LH_AWS_ACCOUNT    your account number
* CDK_LH_AWS_REGION     the region to deploy

### Synthesize

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

## Deploying

Now you are ready to deploy to AWS, using the command:

```
$ cdk deploy
```

## Test

If you want to test using Postman, in `tests` folder, there is a json file named `postman_collection.json`.

Open Postman, import this file an replace the variables:
* `base_url`  your AWS url e.g. https://aws ....
* `task_id`  after creating a task, use the returned id to test the other endpoints.
