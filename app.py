#!/usr/bin/env python3

from aws_cdk import core

from sfn.sfn_stack import SfnStack

app = core.App()

sfn_stack = SfnStack(app, "cdk-sfn")

app.synth()
