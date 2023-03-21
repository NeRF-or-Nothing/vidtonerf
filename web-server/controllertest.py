from flask import Flask, request, make_response, send_file, send_from_directory, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return "this is an html string!"

app.run(host="0.0.0.0", port = 69)
