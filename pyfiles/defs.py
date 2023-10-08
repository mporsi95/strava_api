import requests
import urllib3

from keys import CLIENT_ID, CLIENT_SECRET
from oauthlib.oauth2 import WebApplicationClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## Authorize Strava API
def authorize_strava() -> str:
    '''Authorize Strava API
    Input: None
    Output: Authorization URL
    '''
    # Set url
    auth_url = 'https://www.strava.com/oauth/authorize'

    # Set client
    client = WebApplicationClient(CLIENT_ID)

    # Set authorization url
    url = client.prepare_request_uri(
            auth_url,
            redirect_uri = 'http://localhost:8080',
            scope = ['activity:read_all'],
            approval_prompt = 'force'
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
















## Request token from Strava API
def request_token() -> dict:
    '''Request token from Strava API
    Input: client_id, client_secret, code
    Output: token

    Examples:

    >>> request_token('114849', 'e27bf5a173ce3bcd101be0b49de75143182147f9', '595b13cadcdced379b4dabb36de42f5ecf5f8e3c')
    '''
    # Set url
    auth_url = "https://www.strava.com/oauth/authorize"

    # Set payload
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'f': 'json',
        'scope': 'read_all,profile:read_all,activity:read_all,activity:write'
    }

    print("Requesting Token...\n")

    # Post request
    response = requests.get(auth_url, data = payload, verify = False)

    # Check for errors
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        return None

    # Return token
    return response.json()['access_token']


# activites_url = "https://www.strava.com/api/v3/athlete/activities"



## Get data from Strava API
def get_data_strava(url: str, access_token: str) -> dict:
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