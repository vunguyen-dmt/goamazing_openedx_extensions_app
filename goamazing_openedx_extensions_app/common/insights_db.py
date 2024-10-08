import os
import pyodbc
import logging

log = logging.getLogger('InsightsDatabase')

connection_data = str.split(os.environ.get('INSIGHTS_DATABASE_CONNECTION', ''), ';') # server;dbname;user;password;driver

server = connection_data[0]
database = connection_data[1]
username = connection_data[2]
password = connection_data[3]
driver = connection_data[4]

class InsightsDatabase:
    def __init__(self):
        self.connection = None

    def connect(self):
        """Establish a connection to the database."""
        try:
            self.connection = pyodbc.connect(
                f'DRIVER={driver};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'UID={username};'
                f'PWD={password}'
            )
        except Exception as ex:
            log.error("error connecting insights db: " + str(ex))

    def execute_query(self, query, params, fetchone):
        """Execute a SELECT query and return the results."""
        if not self.connection:
            return None

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            results = cursor.fetchone() if fetchone else cursor.fetchall()
            return results
        except Exception as ex:
            log.error("error executing query on insights db: " + str(ex))
            return None
        finally:
            cursor.close()

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
