#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.cdk_stack import EcsStack


app = cdk.App()
EcsStack(app, "EcsStack", env=cdk.Environment(account='183235224200', region='eu-central-1'))
app.synth()
