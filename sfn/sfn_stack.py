from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.core as core
import aws_cdk.aws_stepfunctions as stepfunctions
import aws_cdk.aws_stepfunctions_tasks as tasks
import aws_cdk.aws_lambda as lambda_


class SfnStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # stepfunctions.Wait(self, "Wait", stepfunctions.WaitTime.duration(core.Duration.seconds(5)))

        flip_coin = lambda_.Function(self,
                                     "FlipCoin",
                                     runtime=lambda_.Runtime.PYTHON_3_8,
                                     handler="index.handler",
                                     code=lambda_.Code.from_asset("./sfn/lambda/flip_coin"))

        flip_coin_invoke = tasks.LambdaInvoke(self,
                                              "FlipCoinInvoke",
                                              lambda_function=flip_coin)

        wait = stepfunctions.Wait(self,
                                  "Wait",
                                  time=stepfunctions.WaitTime.duration(core.Duration.seconds(5)))

        choice = stepfunctions.Choice(self,
                                      "HeadsTailsChoice") \
            .when(condition=stepfunctions.Condition.string_equals("$.input.Payload.result", "heads"),
                  next=stepfunctions.Succeed(self, "Succeed")) \
            .when(condition=stepfunctions.Condition.string_equals("$.input.Payload.result", "tails"),
                  next=flip_coin_invoke)

        stepfunctions.StateMachine(self,
                                   "StateMachine",
                                   definition=flip_coin_invoke.next(wait.next(choice)))
