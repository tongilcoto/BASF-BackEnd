from helpers.schema_controller import *
import requests
from copy import deepcopy
from requests.auth import HTTPBasicAuth
from challenge_urls import *


def get_endpoint(endpoint):
    endpoints = {
        "create": {"path": PERSON, "method": "put"},
        "details": {"path": PERSON_DETAILS, "method": "get"},
        "list": {"path": PERSON_ALL, "method": "get"}
    }
    return endpoints[endpoint]


def get(context, endpoint, *args):
    url = BASE_URL + get_endpoint(endpoint)['path']
    if endpoint == 'details':
        url = url.format(id=context.person_id)
    print(url)
    response = requests.get(url,
                            headers={'accept': '*/*'},
                            auth=HTTPBasicAuth(context.user, context.password)
                            )
    print(response)
    print(response.json())

    context.response_status = response.status_code
    context.response = deepcopy(response.json())


def send(context, endpoint, method):
    send_function = {
        "post": requests.post,
        "put": requests.put
    }
    url = BASE_URL + get_endpoint(endpoint)['path']
    if endpoint == 'details':
        # KO testing
        url = url.format(id='1')
    print(url)
    print(f"Body: {context.person}")
    response = send_function[method](url,
                                     json=context.person,
                                     headers={'accept': '*/*'},
                                     auth=HTTPBasicAuth(context.user, context.password)
                                     )
    print(response)
    print(response.json())

    context.response_status = response.status_code
    context.response = deepcopy(response.json())
