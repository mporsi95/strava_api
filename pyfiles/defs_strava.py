import requests
import urllib3

from keys import CLIENT_ID, CLIENT_SECRET
from oauthlib.oauth2 import WebApplicationClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## Authorize Strava API
def authorize(scope: str) -> str:
    '''Authorize Strava API
    Input: None
    Output: Authorization URL
    '''

    # Set scopes
    scopes = {
        'profile': 'profile:read_all',
        'activity': 'activity:read_all'
    }

    # Set url
    auth_url = 'https://www.strava.com/oauth/authorize'

    # Set client
    client = WebApplicationClient(CLIENT_ID)

    # Set authorization url
    url = client.prepare_request_uri(
            auth_url,
            redirect_uri = 'http://localhost:8080',
            scope = scopes.get(scope),
            approval_prompt = 'auto'
    )

    print(f'Siga o link para autorizar e anote o código: \n {url}')
    code = input('\n Insira o código: ')

    data = client.prepare_request_body(
                code = code,
                redirect_uri = 'http://localhost:8080',
                client_id = CLIENT_ID,
                client_secret = CLIENT_SECRET
            )

    # Post request
    token_url = 'https://www.strava.com/api/v3/oauth/token'
    response = requests.post(token_url, data=data)
    
    # Check for errors
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        return None

    # Return token
    return response.json()['access_token']

## Get data from Strava API
def get_data(url: str, access_token: str) -> dict:
    '''Get data from Strava API
    Input: url
    Output: data from Strava API

    Examples:

    >>> get_data_strava('https://www.strava.com/api/v3/athlete')
    '''
    # Set headers
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Get data from url
    response = requests.get(url, headers = headers)

    # Check for errors
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        return None

    # Convert data to json
    data = response.json()
    return data