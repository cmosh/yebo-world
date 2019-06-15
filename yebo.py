from flask import Flask
import random
import pyodbc
import os
from dotenv import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)

connection_string= "DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};PORT={port}; DATABASE={database};UID={user};PWD={passwd}".format(
                    server=os.getenv('DB_SERVER'),
                    port=os.getenv('DB_PORT'),
                    database=os.getenv('DB_NAME'),
                    user=os.getenv('DB_USER'),
                    passwd=os.getenv('DB_PASS')
)

print(connection_string)
cnxn = pyodbc.connect(connection_string)
cursor = cnxn.cursor()

cursor.execute("""
               SELECT
                yebo.dbo.greetings.greeting  as greeting
                 FROM yebo.dbo.greetings
                """)

greetings = list(cursor)


app = Flask(__name__)
@app.route("/")
def hello():
    hello_world = random.choice(greetings).greeting + " world!"
    return hello_world.capitalize()

if __name__ == '__main__':
    app.run()