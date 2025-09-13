from flask import Flask, render_template, session, abort, redirect, url_for
import pathlib,os
from google_auth_oauthlib.flow import Flow

app = Flask("Studsight")
app.secret_key = "davidneastudsightkey.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")


GOOGLE_CLIENT_ID = "771970138692-gjilmd2o08eitr81o07oiuhfe7m5ardh.apps.googleusercontent.com"

# Example initialization (update with your actual client secrets file and scopes)
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://nea-studsight.onrender.com/callback"
    
    )


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            abort(401) # Authorisation required
        else:
            return function()
        
    return wrapper




@app.route("/login") # Login route
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback") # Callback route
def callback():
    pass


@app.route("/logout") # Logout route
def logout():
    session.clear()
    return redirect("/")


@app.route("/") # Home route
def home():
    return render_template("home.html")


@app.route("/protected_area")
@login_is_required
def protected_area():
    return render_template("protected_area.html", email=session["google_id"])


if __name__ == "__main__": # Run the app
    app.run(debug=True)
