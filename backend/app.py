# save this as app.py
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return jsonify("Hello there!")

@app.route("/update", methods=["POST"])
def update():
    data = request.form
    print(data)
    # convert data to dict
    data = dict(data)


    row = int(data['row'])
    col = int(data['col'])
    val = int(data['val'])

    # read excel file
    df = pd.read_excel("datasheet.xlsx")

    # update value
    df.loc[row, col] = val

    # save to excel file
    df.to_excel("datasheet.xlsx", index=False)

    return jsonify("Success")

if __name__ == '__main__':
    app.run(debug=True)
