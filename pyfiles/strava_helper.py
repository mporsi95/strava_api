import requests
import urllib3
import mysql.connector

from oauthlib.oauth2 import WebApplicationClient
from keys import CLIENT_ID, CLIENT_SECRET, MYSQL_USER, MYSQL_PASSWORD

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class StravaAPI():
    def __init__(self):
        '''Initialize Strava API
        Input: scope
        Output: None
        '''
        # Set keys
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.MYSQL_USER = MYSQL_USER
        self.MYSQL_PASSWORD = MYSQL_PASSWORD

        # Set access tokens
        self.ACCESS_TOKENS = dict()

        # Connect to MySQL database
        self.connect_mySQL()
        

    ## Authorize Strava API
    def authorize(self, scope: str, athlete_id: str) -> str:
        '''Authorize Strava API
        Input: None
        Output: Authorization URL
        '''
        
        check_query = f'''
            select tkn_acesso_{scope} from atletas where id = '{athlete_id}'
        '''

        cursor = self.mysql_connection.cursor()
        cursor.execute(check_query)
        data = cursor.fetchone()

        # if data[0] is not None:
        #     return
        
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
        response = requests.post(token_url, data=data)
        
        # Check for errors
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            return None

        # Set access token
        self.ACCESS_TOKENS[scope] = response.json()['access_token']

        # update_query = f'''
        #     update atletas
        #     set access_token_{scope} = '{self.ACCESS_TOKENS[scope]}'
        #     where id = '{athlete_id}'
        # '''

        # self.execute_query(update_query)

        return

    ## Get data from Strava API
    def get_data(self, url: str, url_type: str) -> dict:
        '''Get data from Strava API
        Input: url
        Output: data from Strava API

        Examples:

        >>> get_data_strava('https://www.strava.com/api/v3/athlete')
        '''
        # Set headers
        headers = {
            'Authorization': f'Bearer {self.ACCESS_TOKENS[url_type]}'
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
    
    def connect_mySQL(self):
        '''Connect to MySQL database
        Input: None
        Output: connection object
        '''

        # Connect to MySQL database
        self.mysql_connection = mysql.connector.connect(
            host = 'localhost',
            database = 'db_strava',
            user = self.MYSQL_USER,
            password = self.MYSQL_PASSWORD
        )

        # Set autocommit
        self.mysql_connection.autocommit = True

        return 
    
    
    def execute_query(self, query: str) -> None:
        '''Execute query
        Input: query
        Output: None
        '''

        cursor = self.mysql_connection.cursor()
        cursor.execute(query)
        return

    def get_athlete_by_id(self, athlete_id: int) -> dict:
        '''Get athlete by id
        Input: athlete_id
        Output: athlete data
        '''
        
        query = '''
            select * from atletas where id = '{athlete_id}'
        '''

        cursor = self.mysql_connection.cursor()
        cursor.execute(query)
        data = cursor.fetchone()

        return data