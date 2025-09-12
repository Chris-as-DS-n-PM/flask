from flask import Flask
app = Flask("Studsight")
app.secret_key = "davidneastudsightkey.com"

@app.route('/')
def hello_world():
    return 'Welcome to studsight!'

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
    return render_template("index.html")

@app.route("/protected_area") 
def protected_area():
    pass

if __name__ == "__main__": # Run the app
    app.run(debug=True)