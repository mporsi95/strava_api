import requests
import urllib3

from oauthlib.oauth2 import WebApplicationClient
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class StravaAPI:
    def __init__(self, athlete_id: str, client_id: str, client_secret: str):
        '''Initialize Strava API
        Input: scope
        Output: None
        '''
        # Set keys
        self.client_id = client_id
        self.client_secret = client_secret
        self.athlete_id = athlete_id

        # Set access tokens
        self.access_tokens = dict()

    ## Authorize Strava API
    def authorize(self, scope: str) -> str:
        '''Authorize Strava API
        Input: None
        Output: Authorization URL
        '''
        
        # Check scope
        if scope not in ['profile', 'activity']:
            print('Escopo inválido. Valores aceitos: profile, activity')
            return None
            
        # Set scopes
        scopes = {
            'profile': 'profile:read_all',
            'activity': 'activity:read_all'
        }

        # Set url
        auth_url = 'https://www.strava.com/oauth/authorize'

        # Set client
        client = WebApplicationClient(self.client_id)

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
                    client_id = self.client_id,
                    client_secret = self.client_secret
                )

        # Post request
        token_url = 'https://www.strava.com/api/v3/oauth/token'
        response = requests.post(token_url, data = data)
        
        # Check for errors
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            return None

        # Set access token
        self.access_tokens[scope] = response.json()['access_token']

        return response