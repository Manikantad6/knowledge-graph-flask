from flask import Flask, request, make_response, render_template
import pandas as pd
import os
from handlers import networkxHandler

app = Flask(__name__)


@app.route("/")
def hello():
    graph_exists = os.path.exists('static/graph.png')
    # print("existis " +graph_exists)
    return render_template('index.html', graph_exists=graph_exists)


@app.route("/addNodes", methods=["GET", "POST"])
def getForm():
    if request.method == "GET":
        return render_template("form.html")
    else:
        print(request.files)
        file = request.files['file']
        print(file.filename)
        if file:
            df = pd.read_csv(file)
            first_two_rows = df.head(2)
            print(first_two_rows)
            networkxHandler.create_graph_image(df)
        return render_template("form.html", status=True)



# =================JUST FOR EXPERIMENT PURPOSE, IGNORE PLEASE===============================
 
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

