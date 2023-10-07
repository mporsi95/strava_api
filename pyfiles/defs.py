import requests
import urllib3

from keys import client_id, client_secret, refresh_token

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## Request token from Strava API
def request_token() -> dict:
    '''Request token from Strava API
    Input: client_id, client_secret, code
    Output: token

    Examples:

    >>> request_token('114849', 'e27bf5a173ce3bcd101be0b49de75143182147f9', '595b13cadcdced379b4dabb36de42f5ecf5f8e3c')
    '''
    # Set url
    auth_url = "https://www.strava.com/oauth/token"

    # Set payload
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'f': 'json'
    }

    print("Requesting Token...\n")

    # Post request
    response = requests.post(auth_url, data = payload, verify = False)

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
def get_data_strava(url: str) -> dict:
    '''Get data from Strava API
    Input: url
    Output: data from Strava API

    Examples:

    >>> get_data_strava('https://www.strava.com/api/v3/athlete')
    '''
    # Set headers
    headers = {
        # 'Authorization': f'Bearer {key}'
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