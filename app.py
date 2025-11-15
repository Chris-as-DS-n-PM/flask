# app_flask.py
from flask import Flask, render_template, request
import requests
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

FASTAPI_URL = "https://fastapi-3qc2.onrender.com/predict"

@app.route("/")
def index():
    return render_template("form.html")

@app.route("/predict", methods=["POST"])
def predict():
    # Récupérer les données du formulaire HTML
    sepal_length = float(request.form["sepal_length"])
    sepal_width = float(request.form["sepal_width"])
    petal_length = float(request.form["petal_length"])
    petal_width = float(request.form["petal_width"])

    # Envoyer les données à l’API FastAPI
    payload = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width
    }

    response = requests.post(FASTAPI_URL, json=payload)
    prediction = response.json().get("prediction", "Erreur")

    # Afficher le résultat sur la page
    return render_template("result.html", prediction=prediction)


def get_connection():
    conn = psycopg2.connect(database="postgresql_test_cttl",
                            user="postgresql_test_cttl_user",
                            password="wKgWpaJ25ENGcxN70T4KQ8EOuuiwdHti",
                            host="dpg-d3ucjhogjchc73a80ksg-a")
    return conn

# ------- Creation-------
@app.route("/init")
def init():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    result = "done"
    return render_template("init.html", result=result)


# ------- INSERT-------
@app.route("/insert")
def insert():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
    '''INSERT INTO users (name) VALUES \
    ('chris'), ('Steph'), ('Bernard');''')
    
    cur.close()
    conn.close()
    result = "done"
    return render_template("insert.html", result=result)


# ------- READ-------
@app.route("/read")
def read():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''SELECT * FROM users''')
    # Fetch the data
    data = cur.fetchall()
    
    cur.close()
    conn.close()
    result = "done"
    return render_template("insert.html", data=data)




