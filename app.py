from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h2>Hello, Your backend application is running.!</h2>"

@app.route("/add/node", methods=["GET", "POST"])
def addNode():
    if request.method == "POST":
        return "<p>adding node POST</p>"
    else:
        return "<p>GET method for add</p>"
    
# hit the beolow following url:http://127.0.0.1:5000/query/what is the capital of karnataka?
@app.route("/query/<text>")
def query(text):
    return f"<p>Given query: <i>{text}</i></p>"




