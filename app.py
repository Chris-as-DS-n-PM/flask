from flask import Flask, render_template, redirect, jsonify, request
import json
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

print("start connection to db")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://robert:LTrCCDwSsyrNhFKffv5TewRi1TQXX9Hs@dpg-cn3qur5jm4es73bmkga0-a.frankfurt-postgres.render.com/recordingsdatabase'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
print("connected to db")

class Recording(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    data = db.Column(db.Text)  # This stores JSON data as text

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "data": self.data
        }

with app.app_context():
    print("Creating database tables...")
    # db.drop_all() delete all tables for dev only
    db.create_all()
    print("Tables created.")

# My recordings JS to Flask RESTful API
recordings = {}


@app.route('/')
def hello_world():
    return render_template("home.html", my_rec=recordings)


if __name__ == "__main__":
    print("Starting application...")
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# SAVE, DELETE, SHOW

# Database integration



def jsonify_recordings(recordings):
    result = []
    for recording in recordings:
        result.append({
            "id": recording.id,
            "name": recording.name,
            "data": recording.data
        })
    return result



@app.route('/saveRecording', methods=["POST"])
def saveRecording():
    data = request.get_json()  # This is your dataOfClicks from the frontend
    print(data)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Assuming you want to use the name as a unique identifier for now, but you could modify this
    name = data.get('name', 'Unnamed Recording')
    recording_data = json.dumps(data.get('clicks', []))  # Convert the clicks list to a JSON string

    new_recording = Recording(name=name, data=recording_data)
    db.session.add(new_recording)
    db.session.commit()

    return jsonify({"status": "OK", "id": new_recording.id})

@app.route('/list-recordings', methods=['GET'])
def list_recordings():
    recordings = Recording.query.order_by(Recording.id).all()  # Fetch all recordings from the database, + sort recordings by ID
    return jsonify([recording.serialize() for recording in recordings])

@app.route('/rename-recording', methods=['POST'])
def rename_recording():
    data = request.get_json()
    if not data or 'id' not in data or 'newName' not in data:
        return jsonify({"error": "Invalid request"}), 400

    recording = Recording.query.get(data['id'])
    if recording:
        recording.name = data['newName']
        db.session.commit()
        return jsonify({"success": True, "id": recording.id, "newName": recording.name})
    else:
        return jsonify({"error": "Recording not found"}), 404

@app.route('/delete-recording', methods=['POST'])
def delete_recording():
    data = request.get_json()
    if not data or 'id' not in data:
        return jsonify({"error": "Invalid request"}), 400

    recording = Recording.query.get(data['id'])
    if recording:
        db.session.delete(recording)
        db.session.commit()
        return jsonify({"success": True, "id": data['id']})
    else:
        return jsonify({"error": "Recording not found"}), 404
