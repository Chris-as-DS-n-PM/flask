from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/berlin-data")
def berlin_data():
    data = [
        {
            "category": "Fußballverein",
            "name": "FC Viktoria 1889 Berlin",
            "email": "vereinsverwaltung@viktoria.berlin",
            "district": "Tempelhof-Schöneberg",
            "source": "https://viktoria.berlin"
        },
        {
            "category": "Kita",
            "name": "INA.KINDER.GARTEN Prenzlauer Berg",
            "email": "prenzlauerberg@inakindergarten.de",
            "district": "Pankow",
            "source": "https://inakindergarten.de"
        },
        {
            "category": "Private Schule",
            "name": "Berlin Metropolitan School",
            "email": "info@metropolitanschool.com",
            "district": "Mitte",
            "source": "https://metropolitanschool.com"
        }
    ]
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
