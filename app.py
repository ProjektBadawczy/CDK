#!/usr/bin/env python3
import aws_cdk as cdk
from cdk.microservices_stack import MicroservicesStack
from cdk.monolith_stack import MonolithStack

app = cdk.App()
MonolithStack(app, "EcsMonolithStack", env=cdk.Environment(account='183235224200', region='eu-central-1'))
MicroservicesStack(app, "EcsMicroservicesStack", env=cdk.Environment(account='183235224200', region='eu-central-1'))
app.synth()
