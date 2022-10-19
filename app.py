from flask import Flask
from flask import request

import data

app = Flask(__name__)

@app.route("/search", methods=["GET"])
def search():
    db = data.SqliteDB()
    res = db.search(ein=request.json.get("EIN"), comp=request.json.get("COMPANY"))
    return res

