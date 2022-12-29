#!/usr/bin/env python3
import aws_cdk as cdk
from cdk.stacks.microservices_stack import MicroservicesStack
from cdk.stacks.monolith_stack import MonolithStack

app = cdk.App()
MonolithStack(app, "MonolithStack", env=cdk.Environment(account='736936197866', region='eu-central-1'))
MicroservicesStack(app, "MicroservicesStack", env=cdk.Environment(account='736936197866', region='eu-central-1'))
app.synth()
