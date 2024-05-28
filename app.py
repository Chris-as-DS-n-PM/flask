import os
import psycopg2

from flask import Flask
app = Flask(__name__)

conn = psycopg2.connect(dbname='test_jpgf', user='test_jpgf_user', password='RCYokXSELN3K7Tjtr249F5lh6qz4Pnga', host='dpg-cpasrdtds78s73d7k3ag-a.frankfurt-postgres.render.com', port='5432', sslmode='require')

SELECT = """SELECT * FROM test;"""

@app.route('/')
def hello_world():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(SELECT)
            average = cursor.fetchone()[0]
    return "Hello World " + str(average)

@app.route('/vhvh')
def vhvh():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT * FROM test WHERE nom = 'vhvh';""")
            average = cursor.fetchone()[0]
    return "Hello World " + str(average)
