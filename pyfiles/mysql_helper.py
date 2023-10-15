import mysql.connector

from keys import MYSQL_USER, MYSQL_PASSWORD

class MySQLHelper():
    def __init__(self):
        '''Initialize MySQL Helper
        Input: None
        Output: None
        '''

        # Set keys
        self.MYSQL_USER = MYSQL_USER
        self.MYSQL_PASSWORD = MYSQL_PASSWORD

        # Set connection
        self.mysql_connection = None

        # Connect to MySQL database
        self.connect_mySQL()

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

        print(f'Connected successfully to {self.mysql_connection.database}')
        return 
    
    
    def execute_query(self, query: str) -> None:
        '''Execute query
        Input: query
        Output: None
        '''

        cursor = self.mysql_connection.cursor(dictionary = True)
        cursor.execute(query)
        cursor.close()
        return

    def get_athlete_by_id(self, athlete_id: int) -> dict:
        '''Get athlete by id
        Input: athlete_id
        Output: athlete data
        '''
        
        query = f'''
            select * from atletas where id = '{athlete_id}'
        '''

        cursor = self.mysql_connection.cursor(dictionary = True)
        cursor.execute(query)
        data = cursor.fetchone()
        cursor.close()

        return data

    def insert_data(self, table: str, data: dict) -> None:
        try:

            # Gere a parte da consulta SQL com os nomes das colunas e marcadores de posição
            columns = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))

            # Crie a consulta SQL completa
            sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"
            print(sql)
            # Extraia os valores dos dados e os coloque em uma tupla
            valores = tuple(data.values())

            # Execute a consulta com os valores
            cursor = self.mysql_connection.cursor(dictionary = True)
            cursor.execute(sql, valores)
            cursor.close()

            print("Insert concluded successfully!")

        except mysql.connector.Error as err:
            print(f"Error MySQL: {err}")
    

    def update_access_token(self, athlete_id: str, scope: str, token: str) -> None:
        '''Update access tokens
        Input: scope
        Output: None
        '''
        
        query = f'''
            update atletas
            set tkn_acesso_{scope} = '{token}'
            where id = '{athlete_id}'
        '''

        self.execute_query(query)

        return