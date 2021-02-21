from behave import given, when, then, use_step_matcher
from os import environ
import requests
import rstr
import re
from requests.auth import HTTPBasicAuth
from challenge_urls import *
from helpers.challenge_requests import get_endpoint, get, send
from helpers.schema_controller import get_response_schema
from openapi_schema_validator import validate
from jsonpath_ng.ext import parse
from hamcrest import assert_that, equal_to


@given('I am an authorised api consumer')
def step_authorised(context):
    context.user = environ.get('QKNOWS_BACKEND_USER')
    context.password = environ.get('QKNOWS_BACKEND_PASSWORD')


@when('I ask for all persons')
def step_get_all(context):
    get(context, "list")


@when('I create a new complete person')
def step_complete_person(context):
    context.person = {"firstName": rstr.rstr('ABCDEFghij', 5), "lastName": rstr.rstr('ABCDEFghij', 5)}
    send(context, 'create', 'put')


@when('I create a new complete person with special characters')
def step_complete_person_special_chars(context):
    context.person = {"firstName": "ÁªÀÄÂÃÅĄÆáàäâãåąæßÇĆČçćčÑñ'ÉÈËÊĘĖĒéèëêęėē",
                      "lastName": "ŠšÍÏÌÎĮĪíïìîįīÓºÒÖÔÕØŒŌóºòöôõøœōÚÜÙÛŪúüùûū"}
    send(context, 'create', 'put')


@then('I can retrieve created person')
def step_created_person_ok(context):
    context.person_id = context.response['id']
    get(context, "details")
    step_response_ok(context, "details")
    context.person['id'] = context.person_id
    assert_that(context.response, equal_to(context.person))


@when('I send a get request to a wrong endpoint')
def step_wrong_endpoint(context):
    url = BASE_URL + PERSON + "wrong"
    print(url)
    response = requests.get(url,
                            headers={'accept': '*/*'},
                            auth=HTTPBasicAuth(context.user, context.password)
                            )
    print(response)
    context.response_status = response.status_code


@when('I create an invalid person by "{error}" error')
def step_invalid_data(context, error):
    include, field = re.search(r'([\w]+) at ([\w]+)', error).group(1, 2)
    include_value_first = ''
    include_value_second = ''
    if field == 'firstName':
        include_value_first = ('#', '5')[include == 'numbers']
    else:
        include_value_second = ('#', '5')[include == 'numbers']
    context.person = {
        "firstName": rstr.rstr('ABCDEFghij', 5, include=include_value_first),
        "lastName": rstr.rstr('ABCDEFghij', 5, include=include_value_second)
    }
    send(context, 'create', 'put')


use_step_matcher("re")


@when('I send a "(?P<method>get|put|post)" request to "(?P<endpoint>create|list|details)" endpoint')
def step_wrong_method(context, method, endpoint):
    if method == 'get':
        request_function = get
    else:
        request_function = send
        context.person = {"person": "no person"}
    request_function(context, endpoint, method)


@when('I create an invalid person by missing "(?P<field>firstName|lastName|all)" data')
def step_invalid_data(context, field):
    if field == 'all':
        context.person = {}
    else:
        context.person = {"firstName": rstr.rstr('ABCDEFghij', 5), "lastName": rstr.rstr('ABCDEFghij', 5)}
        del context.person[field]
    send(context, 'create', 'put')


@then('I get a "(?P<endpoint>create|list|details)" OK response with matching schema')
def step_response_ok(context, endpoint):
    assert context.response_status == 200
    endpoint = get_endpoint(endpoint)
    schema = get_response_schema(endpoint['path'], endpoint['method'], "200")
    validate(context.response, schema)


@then('I get a "(?P<error>404|405|422)" error')
def step_response_ko(context, error):
    assert_that(context.response_status, equal_to(int(error)))
