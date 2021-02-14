import aws_cdk.core as core
import aws_cdk.aws_stepfunctions as stepfunctions
import aws_cdk.aws_stepfunctions_tasks as tasks
import aws_cdk.aws_lambda as lambda_


class SfnStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        flip_coin_function = lambda_.Function(self,
                                              "FlipCoinFunction",
                                              runtime=lambda_.Runtime.PYTHON_3_8,
                                              handler="index.handler",
                                              code=lambda_.Code.from_asset("./sfn/lambda/flip_coin"))

        flip_coin_invoke = tasks.LambdaInvoke(self,
                                              "FlipCoin",
                                              lambda_function=flip_coin_function)

        wait = stepfunctions.Wait(self,
                                  "Wait",
                                  time=stepfunctions.WaitTime.duration(core.Duration.seconds(5)))

        tails_result = stepfunctions.Pass(self, "TailsResult")
        tails_result.next(flip_coin_invoke)

        choice = stepfunctions.Choice(self,
                                      "HeadsTailsChoice") \
            .when(condition=stepfunctions.Condition.string_equals("$.Payload.result", "heads"),
                  next=stepfunctions.Succeed(self, "HeadsResult")) \
            .when(condition=stepfunctions.Condition.string_equals("$.Payload.result", "tails"),
                  next=tails_result)

        stepfunctions.StateMachine(self,
                                   "StateMachine",
                                   definition=flip_coin_invoke.next(wait.next(choice)))
