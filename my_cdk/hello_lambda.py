from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_logs as logs,
    RemovalPolicy,
    aws_iam as iam,
    aws_scheduler as scheduler
)
from constructs import Construct
from typing import cast

class Hello_Lambda_CDK_Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket_name = "jitendra-lambda-bucket"
        object_key = "mylambda.zip"

        # Define a log group for the Lambda function
        log_group = logs.LogGroup(
            self, f"HelloLambdaFN-LogGroup-ID",
            log_group_name=f"/aws/lambda/HelloLambdaFN-LogGroup",
            removal_policy=RemovalPolicy.DESTROY,
            retention=logs.RetentionDays.THREE_DAYS
        )

        # Define a Lambda function resource here
        my_lambda = _lambda.Function(
            self, f"HelloLambdaFN-ID",
            runtime=_lambda.Runtime.PYTHON_3_13,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_bucket( 
                bucket = s3.Bucket.from_bucket_name(self, f"HelloLambdaFN-Bucket-ID", bucket_name),
                key = object_key
            ),
            log_group=log_group,
            timeout=Duration.seconds(30),
            memory_size=128,
            function_name="HelloLambdaFN"
        )

        schedular_role = iam.Role(
            self, "HelloLambdaFN-SchedulerRole",
            assumed_by=cast(iam.IPrincipal, iam.ServicePrincipal("scheduler.amazonaws.com"))
        )

        schedular_role.add_to_policy(
            iam.PolicyStatement(
                actions=["lambda:InvokeFunction"],
                resources=[my_lambda.function_arn]
            )
        )

        scheduler.CfnSchedule(
            self, "HelloLambdaFN-Schedule",
            name="HelloLambdaFN-Schedule",
            flexible_time_window=scheduler.CfnSchedule.FlexibleTimeWindowProperty(
                mode="OFF"
            ),
            schedule_expression="cron(0 9 * * ? *)",  # Every day at 12:00 UTC
            description="Schedule to invoke HelloLambdaFN every day at 12:00 UTC",
            state="ENABLED",
            schedule_expression_timezone="PST",
            target=scheduler.CfnSchedule.TargetProperty(
                arn=my_lambda.function_arn,
                role_arn=schedular_role.role_arn
            )
        )

        # Add permissions for the Lambda function to write to the log group
        log_group.grant_write(my_lambda)

        # Add permissions for the Lambda function to read from the S3 bucket
        # s3.Bucket.from_bucket_name(self, f"HelloLambdaFN-Bucket-ID", bucket_name).grant_read(my_lambda)

        

        
        
