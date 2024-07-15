from flask import Flask, request, make_response, render_template
import pandas as pd
import os
from handlers import networkxHandler
from handlers import neo4jHandler

app = Flask(__name__)

# ===========network x realted routes=====================
@app.route("/")
def index():
    graph_exists = os.path.exists('static/graph.png')
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

#================ Neo4J related routes ==================================
@app.route("/neo")
def neo():
    result = neo4jHandler.queryGeoDB()
    return render_template("interactive.html", response=result)
   


@app.route("/neo/import", methods=["GET", "POST"])
def get_neo4j_form():
    if request.method == "GET":
        return render_template("neo4jForm.html")
    else:
        print(request.files)
        file = request.files['file']
        print(file.filename)
        if file:
            df = pd.read_csv(file)
            first_two_rows = df.head(2)
            print(first_two_rows)
            neo4jHandler.insertFromCSV(df)
        return render_template("neo4jForm.html", status=True)
    

@app.route("/neo/deleteAllNodes")
def deleteNodes():
    neo4jHandler.delete_data()
    return 'Deleted nodes'




