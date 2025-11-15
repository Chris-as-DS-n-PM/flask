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
    url = os.getenv("DATABASE_URL")

    # Render fournit parfois `postgres://` → psycopg2 accepte les deux
    return psycopg2.connect(url, cursor_factory=RealDictCursor)

@app.route("/init")
def init():
    conn = get_connection()
    cur = conn.cursor()
    return render_template("init.html")
