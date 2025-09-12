from flask import Flask, render_template, session, abort 
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
    pass

@app.route("/callback") # Callback route
def callback():
    pass#

@app.route("/logout") # Logout route
def logout():
    pass

@app.route("/") # Home route
def index():
    return "hi." 

@app.route("/protected_area")
@login_is_required
def protected_area():
    pass

if __name__ == "__main__": # Run the app
    app.run(debug=True)
