import sys
import os

def before_all(context):
    context.endpoint = f"http://{context.config.userdata.get('apiEndpoint')}:{context.config.userdata.get('apiPort')}"