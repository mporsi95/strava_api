import requests
import urllib3

from oauthlib.oauth2 import WebApplicationClient
from keys import CLIENT_ID, CLIENT_SECRET
from mysql_helper import MySQLHelper
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class StravaAPI():
    def __init__(self, athlete_id: str):
        '''Initialize Strava API
        Input: scope
        Output: None
        '''
        # Set keys
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.ATHLETE_ID = athlete_id

        # Set access tokens
        self.ACCESS_TOKENS = dict()

        # Set MySQL Helper
        self.MYSQL = MySQLHelper()

        # Check access tokens
        self.check_access_tokens()

    ## Authorize Strava API
    def authorize(self, scope: str, athlete_id: str) -> str:
        '''Authorize Strava API
        Input: None
        Output: Authorization URL
        '''
        
        # Check scope
        if scope not in ['profile', 'activity']:
            print('Escopo inválido. Valores aceitos: profile, activity')
            return None
        
        # Check athlete
        athlete = self.MYSQL.get_athlete_by_id(athlete_id)

        # if athlete & (athlete[f'tkn_acesso_{scope}'] is not None):
        #     self.ACCESS_TOKENS[scope] = athlete[f'tkn_acesso_{scope}']
        #     return
            
        if not athlete:
            # Set scopes
            scopes = {
                'profile': 'profile:read_all',
                'activity': 'activity:read_all'
            }

            # Set url
            auth_url = 'https://www.strava.com/oauth/authorize'

            # Set client
            client = WebApplicationClient(self.CLIENT_ID)

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
                        client_id = self.CLIENT_ID,
                        client_secret = self.CLIENT_SECRET
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
            self.ACCESS_TOKENS[scope] = response.json()['access_token']

        return

    ## Check access tokens
    def check_access_tokens(self) -> None:
        '''Check access tokens
        Input: None
        Output: None
        '''
        
        # Set scopes
        scopes = ['profile', 'activity']

        # Get athlete
        athlete = self.MYSQL.get_athlete_by_id(self.ATHLETE_ID)

        if (athlete is not None) \
            and (athlete['tkn_acesso_perfil'] is not None) \
                and (athlete['tkn_acesso_atividade'] is not None):

            self.ACCESS_TOKENS['profile'] = athlete['tkn_acesso_perfil']
            self.ACCESS_TOKENS['activity'] = athlete['tkn_acesso_atividade']
            return

        # Check athletes
        if not athlete:
            # Authorize profile
            self.create_athlete(self.ATHLETE_ID)
            return
        

        # Check scopes
        for scope in scopes:
            if athlete[f'tkn_acesso_{scope}'] is None:
                self.authorize(scope, self.ATHLETE_ID)
        
        return
        
    ## Create athlete
    def create_athlete(self, athlete_id: str) -> None:
        '''Create athlete
        Input: scope
        Output: None
        '''

        # Check athlete
        athlete = self.MYSQL.get_athlete_by_id(athlete_id)
        if athlete:
            print('Atleta já existe')
            return None
        
        # Set scopes
        scopes = ['profile', 'activity']

        # Get authorizations
        for scope in scopes:
            self.authorize(scope, athlete_id)

        # Get athlete data
        athlete_data = self.get_data('https://www.strava.com/api/v3/athlete', 'profile')
        
        # Insert athlete
        self.MYSQL.insert_data(
            'atletas',
            {
                'id': athlete_data['id'],
                'username': athlete_data['username'],
                'estado_recurso': athlete_data['resource_state'],
                'nome': ' '.join([athlete_data['firstname'], athlete_data['lastname']]),
                'biografia': athlete_data['bio'],
                'cidade': athlete_data['city'],
                'estado': athlete_data['state'],
                'pais': athlete_data['country'],
                'sexo': athlete_data['sex'],
                'peso': athlete_data['weight'],
                'link_foto': athlete_data['profile'],
                'nu_seguidores': athlete_data['follower_count'],
                'nu_amigos': athlete_data['friend_count'],
                'pref_data': athlete_data['date_preference'],
                'pref_medidas': athlete_data['measurement_preference'],
                'ftp': athlete_data['ftp'],
                'tkn_acesso_perfil': self.ACCESS_TOKENS['profile'],
                'tkn_acesso_atividade': self.ACCESS_TOKENS['activity'],
                'dh_criacao': datetime.strptime(athlete_data['created_at'], "%Y-%m-%dT%H:%M:%SZ") \
                                                                    .strftime("%Y-%m-%d %H:%M:%S"),
                'dh_atualizacao': datetime.strptime(athlete_data['updated_at'], "%Y-%m-%dT%H:%M:%SZ") \
                                                                    .strftime("%Y-%m-%d %H:%M:%S"),
                'dh_ingestao': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )

        return
    
    ## Get data from Strava API
    def get_data(self, url: str, scope: str) -> dict:
        '''Get data from Strava API
        Input: url
        Output: data from Strava API

        Examples:

        >>> get_data_strava('https://www.strava.com/api/v3/athlete')
        '''
        # Set headers
        headers = {
            'Authorization': f'Bearer {self.ACCESS_TOKENS[scope]}'
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