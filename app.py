#!/usr/bin/env python3
import os

import aws_cdk as cdk

from eks_repo.eks_repo_stack import EksRepoStack

app = cdk.App()

EksRepoStack(app, "EksRepoStack")

app.synth()
