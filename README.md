# BASF BACKEND CHALLENGE

## Pre-requisites

1. Python version 3 and pip
2. pipenv (pip install pipenv)

## Deployment

1. pipenv install --ignore-pipfile
2. pipenv shell

## Execution

1. export QKNOWS_BACKEND_USER=<api user>
2. export QKNOWS_BACKEND_PASSWORD=<api password>
5. behave --no-capture --json -o reports/report.json

## Exiting virtual env

1. exit


## Tests

- To list all persons of the system
- To create a new person: since the API does not respond with the created object, a second request, a "get" on the given object id, is needed
- To create a new person using special valid consonants and vowels 
- To use invalid characters for person names, such as numbers and symbols
- To try to create a person with missing data, such as firstName, secondName or both
- To try invalid api requests, such as non-existing endpoints or invalid method for a valid endpoint


## Test Results: json report

Results are at reports/report.json file since it is the one configured at behave command line

The results include up to test step status

Disclaimer: 
The api response is matched against provided swagger openapi 3.0 schema. It is stored in a file. But two light modifications were needed
- "Person" schema at "components" is missing "nullable" property. In order to follow current api behaviour, I set it up as "true"
- "schema" property for "/api/person" -> "put" -> "responses" is wrong, since it is defining it as a string and it is a dict.

Results:

- As an api consumer I want to be informed of a person invalid data.feature
  - Failed. 
    - It is not detecting numbers for person names (either first or last) and rejecting it
    - It is not detecting symbols for person names (either first or last) and rejecting it
- As an api consumer I want to be informed of a person missing data.feature
  - Failed
    - It is not detecting missing "firstName" property and rejecting it
    - It is not detecting missing "lastName" property and rejecting it
    - It is possible to create an empty person, i.e. without both "firstName" and "lastName"
- As an api consumer I want to be informed of a wrong endpoint.feature
  - Passed
- As an api consumer I want to be informed of a wrong method.feature
  - Passed
- As an api consumer I want to create a new ordinary person.feature
  - Failed
    - There is a random issue which changes "firstName" value into a new string with twice or three times its value. Example: "abc" -> "abcabc" or "abcabcabc"
- As an api consumer I want to create a new person with special characters.feature
  - Passed
- As an api consumer I want to list all persons.feature
  - Passed
    
