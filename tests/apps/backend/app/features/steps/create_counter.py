from behave import *

from httpx import request
import json

@given('i send a {method} request to \"{path}\" with body')
def step_impl(context, method, path):
    if not method == 'POST':
        assert False
    
    req_body = json.loads(context.text)

    context.response = request(
        method='POST', 
        url=f"{context.endpoint}{path}", 
        json=req_body
    )

@then('the response status code should be {code}')
def step_impl(context, code):
    assert int(code) == context.response.status_code