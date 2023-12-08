from flask import Flask
app = Flask(__name__)

@app.route('/_about')
def about():
    return Response("<?xml version=\"1.0\" encoding=\"UTF-8\" ?><html>about</html>", content_type='text/xml')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/cgi-bin/systemutil.cgi', methods=['POST'])
def system_util():
    params = request.form
    code = "2" if params.get("user") == "admin" and params.get("password") == "admin" else "0"
    response_content = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n" + \
                       "<xml>\n" + \
                       "<Login>{}</Login>\n".format(code) + \
                       "</xml>"
    return Response(response_content, content_type='text/xml')

@app.route('/cgi-bin/modem.cgi', methods=['GET'])
def modem_cgi():
    command = request.args.get("Command")
    if command == "getAntenna":
        response_content = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n" + \
                           "<xml>\n" + \
                           "<antenna_value>2</antenna_value>\n" + \
                           "</xml>\n"
    elif command == "getModemStatus":
        response_content = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n" + \
                           "<xml>\n" + \
                           "<antenna_value>2</antenna_value>\n" + \
                           "</xml>\n"
    else:
        return "Invalid command", 400

    return Response(response_content, content_type='text/xml')
