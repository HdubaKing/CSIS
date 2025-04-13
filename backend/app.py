# save this as app.py
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return jsonify("Hello there!")

@app.route('/new_game', methods=["POST"])
def new_game():
    # Delete old datasheet and replace it with a new one
    data = dict(request.form)
    
    country_list = data['countries'].split(',')

    df = pd.DataFrame(columns=['X']+country_list)

    # First recreate base stats lists
    base_stats = ['Political Power', "GDP", "Budget", "Emissions"]
    base_stats_df = pd.DataFrame(columns=['X']+country_list)
    base_stats_df['X'] = base_stats
    base_stats_df[country_list] = np.zeros([len(base_stats), len(country_list)])

    df = pd.concat([df, base_stats_df], axis=0)

    # Now create Tarriff matrices for each sector + HC/LC
    sectors = ['Resource Extraction', 'Industrial', 'Consumer Goods', 'Agriculture', 'Energy']
    for sector in sectors:
        for intensity in ['High Carbon', 'Low Carbon']:
            sector_df = pd.DataFrame(columns=['X']+country_list)
            sector_df['X'] = [f'{sector} ({intensity})'] + country_list
            
            data = np.zeros([len(country_list)+1, len(country_list)])
            data[0,:] = [np.nan] * data.shape[1]
            sector_df[country_list] = data

            df = pd.concat([df, sector_df], axis=0)

    df.to_excel('datasheet.xlsx')

    return jsonify("success")


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
    df.iloc[row, col] = val
    print(df.iloc[row, col])

    # save to excel file
    df.to_excel("datasheet.xlsx", index=False)

    return jsonify("Success")

if __name__ == '__main__':
    app.run(debug=True)
