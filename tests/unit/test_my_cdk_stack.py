import aws_cdk as core
import aws_cdk.assertions as assertions

from my_cdk.hello_lambda import Hello_Lambda_CDK_Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in my_cdk/my_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Hello_Lambda_CDK_Stack(app, "my-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
