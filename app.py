import os
import psycopg2
#from dotenv import load_dotenv

#load_dotenv()  # loads variables from .env file into environment

from flask import Flask
app = Flask(__name__)

url = os.environ.get("postgres://test_jpgf_user:RCYokXSELN3K7Tjtr249F5lh6qz4Pnga@dpg-cpasrdtds78s73d7k3ag-a.frankfurt-postgres.render.com/test_jpgf")  # gets variables from environment
connection = psycopg2.connect(url)

SELECT = """SELECT * FROM test;"""

@app.route('/')
def hello_world():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT)
            average = cursor.fetchone()[0]
    return 'Hello, World!' + average
