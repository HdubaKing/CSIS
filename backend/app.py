# save this as app.py
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict

app = Flask(__name__)

@app.route("/", methods=["GET"])
def hello():
    return jsonify("Hello there!")

@app.route('/commit', methods=["POST"])
def commit():
    # Get the sheet names from the Excel file
    xls = pd.ExcelFile('datasheet.xlsx')
    sheet_names: List[str] = xls.sheet_names

    turn_sheet_names = [sheet for sheet in sheet_names if 'Turn' in sheet]
    turns = [int(sheet.split(' ')[1]) for sheet in turn_sheet_names]
    max_turn = max(turns) if turns else 0
    new_turn = max_turn + 1

    # Read the current datasheet
    df = pd.read_excel(xls, sheet_name="buffer")

    # Create a new sheet name for the new turn
    new_sheet_name = f"Turn {new_turn}"
    with pd.ExcelWriter('datasheet.xlsx', engine='openpyxl', mode='a') as writer:
        # Write the current datasheet to the new sheet
        df.to_excel(writer, sheet_name=new_sheet_name, index=False)


    return jsonify("success")

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

    with pd.ExcelWriter('datasheet.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="buffer", index=False)
    
    return jsonify("success")

def update_tariff(df, item, intensivity, source, destination, qty):
    search_string = f'{item} ({intensivity} Carbon)'
    
    # Find the row index for the item
    row_index = df[df['X'] == search_string].index[0]

    country_list = df.columns[1:]
    source_idx = country_list.get_loc(source)
    dest_idx = country_list.get_loc(destination)
    
    df.iloc[row_index+source_idx+1, dest_idx+1] = qty

    return df


@app.route("/update", methods=["POST"])
def update():
    data = request.json
    
    xls = pd.ExcelFile('datasheet.xlsx')
    df = pd.read_excel(xls, sheet_name="buffer")

    for item in data:
        if item['type'] == 'tariff':
            df = update_tariff(df, item['item'], item['intensivity'], item['source'], item['destination'], item['qty'])
        else:
            # Handle other types of updates here
            pass

    # Save the updated DataFrame back to the Excel file
    with pd.ExcelWriter('datasheet.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name="buffer", index=False)
        

    return jsonify("Success")

@app.route('/get_last_state', methods=["GET"])
def get_last_state():
    # Get the last turn sheet name
    xls = pd.ExcelFile('datasheet.xlsx')
    sheet_names: List[str] = xls.sheet_names

    turn_sheet_names = [sheet for sheet in sheet_names if 'Turn' in sheet]
    turns = [int(sheet.split(' ')[1]) for sheet in turn_sheet_names]
    max_turn = max(turns) if turns else 0

    # Read the last turn datasheet
    df = pd.read_excel(xls, sheet_name=f"Turn {max_turn}")

    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
