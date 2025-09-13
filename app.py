from flask import Flask, render_template, session, abort, redirect, url_for
app = Flask("Studsight")
app.secret_key = "davidneastudsightkey.com"

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            abort(401) # Authorisation required
        else:
            return function()
        
    return wrapper


@app.route("/login") # Login route
def login():
    session["google_id"] = "example_google_id"
    return redirect("/protected_area")

@app.route("/callback") # Callback route
def callback():
    return "call"

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
