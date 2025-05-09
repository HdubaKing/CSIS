# save this as app.py
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from typing import List, Tuple, Dict

from model import update_buffer

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
    columns = ['X'] + country_list + [''] + country_list

    df = pd.DataFrame(columns=columns)

    # First recreate base stats lists
    base_stats = ['Political Power', "GDP", "Budget", "Emissions"]
    base_stats_df = pd.DataFrame(columns=columns)
    base_stats_df['X'] = base_stats
    
    data = np.zeros([len(base_stats), len(country_list)*2])
    base_stats_df[country_list] = data

    df = pd.concat([df, base_stats_df], axis=0)
    df.iloc[0:len(country_list)+1, len(country_list)+1:] = np.nan

    empty_row_df = pd.DataFrame([[np.nan] * len(df.columns)], columns=df.columns)
    info_row = ["TARRIFFS"] + len(country_list)*[''] + ["EXPORTS"] + len(country_list)*['']
    info_df = pd.DataFrame(data=[info_row], columns=columns)

    df = pd.concat([df, empty_row_df, info_df], axis=0)

    # Now create Tarriff matrices for each sector + HC/LC
    sectors = ['Resource Extraction', 'Industrial', 'Consumer Goods', 'Agriculture', 'Energy']
    for sector in sectors:
        for intensity in ['High Carbon', 'Low Carbon']:
            sector_df = pd.DataFrame(columns=df.columns)
            sector_df['X'] = [f'{sector} ({intensity})'] + country_list
            
            data = np.zeros([len(country_list)+1, len(country_list)*2])
            print(sector_df[country_list].shape)

            data[0,:] = [np.nan] * data.shape[1]
            sector_df[country_list] = data

            df = pd.concat([df, empty_row_df], axis=0)
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

@app.route('/get_country_list', methods=["GET"])
def get_country_list():
    # Get the country list from the Excel file
    xls = pd.ExcelFile('datasheet.xlsx')
    df = pd.read_excel(xls, sheet_name="buffer")

    # Extract the country list from the DataFrame
    country_list = df.columns[1:].tolist()

    return jsonify(country_list)

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

    return jsonify(df.loc[:3,:].to_dict(orient='records'))

@app.route('/get_time_series', methods=["GET"])
def get_time_series():
    data = request.json
    print("AHGHGHGHG", data, type(data))
    xls = pd.ExcelFile('datasheet.xlsx')

    # Get the sheet names from the Excel file
    sheet_names: List[str] = xls.sheet_names
    turn_sheet_names = [sheet for sheet in sheet_names if 'Turn' in sheet]

    # Get all stats corresponding to the given country and item
    country = data['country']
    item = data['item']
    time_series = []

    for sheet in turn_sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        # Find the row index for the item
        row_index = df[df['X'] == item].index[0]
        # Get the value for the given country
        value = df.iloc[row_index][country]
        time_series.append(value)
    
    return jsonify(time_series)

@app.route('/forward_compute_state', methods=["POST"])
def forward_compute_state():
    update_buffer()

# PP Actions
@app.route("/perform_action", methods=["POST"])
def perform_action():
    data = request.json
    country = data['country']
    action = data['action']

    xls = pd.ExcelFile('datasheet.xlsx')
    df = pd.read_excel(xls, sheet_name="buffer")

    # variable extraction
    try:
        gdp = df.loc[df['X'] == 'GDP', country].values[0]
        budget = df.loc[df['X'] == 'Budget', country].values[0]
        emissions = df.loc[df['X'] == 'Emissions', country].values[0]
        pol_power = df.loc[df['X'] == 'Political Power', country].values[0]
    except KeyError:
        return jsonify({"status": "error", "reason": "Country data missing"}), 400

    # Action Definitions
    action_table = {
        "Stimulus Package": {"pp_cost": 2, "money_cost": 200, "effect": lambda g,b,e: (g * 1.03, b - 200, e * 1.01)},
        "Subsidize Industries": {"pp_cost": 3, "money_cost": 250, "effect": lambda g,b,e: (g * 1.00, b - 250, e)},
        "Tax Reform": {"pp_cost": 4, "money_cost": 0, "effect": lambda g,b,e: (g * 1.02, b * 0.95, e)},
        "Green Energy Investment": {"pp_cost": 2, "money_cost": 300, "effect": lambda g,b,e: (g * 1.00, b - 300, e * 0.95)},
        "Deregulation": {"pp_cost": 2, "money_cost": 0, "effect": lambda g,b,e: (g * 1.04, b, e * 1.03)},
        "Infrastructure Bill": {"pp_cost": 4, "money_cost": 400, "effect": lambda g,b,e: (g * 1.05, b - 400, e)},
    }

    if action not in action_table:
        return jsonify({"status": "error", "reason": "Invalid action"}), 400

    act = action_table[action]

    # check to see if enough of rescource
    if pol_power < act['pp_cost']:
        return jsonify({"status": "error", "reason": "Not enough Political Power"}), 400
    if budget < act['money_cost']:
        return jsonify({"status": "error", "reason": "Not enough Money"}), 400

    # effect application 
    new_gdp, new_budget, new_emissions = act['effect'](gdp, budget, emissions)

    # updated spreadsheet
    df.loc[df['X'] == 'GDP', country] = new_gdp
    df.loc[df['X'] == 'Budget', country] = new_budget
    df.loc[df['X'] == 'Emissions', country] = new_emissions
    df.loc[df['X'] == 'Political Power', country] = pol_power - act['pp_cost']

    with pd.ExcelWriter('datasheet.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name="buffer", index=False)

    return jsonify({"status": "success", "new_gdp": new_gdp, "new_budget": new_budget, "new_emissions": new_emissions})



@app.route("/send_chat", methods=["POST"])
def send_chat():
    data = request.get_json()
    sender = data["sender"]
    receiver = data["receiver"]
    message = data["message"]
    timestamp = datetime.now(timezone.utc).isoformat()

    tab_name = f"Chat_{sender}"
    try:
        xls = pd.ExcelFile('datasheet.xlsx')
        if tab_name in xls.sheet_names:
            chat_df = pd.read_excel(xls, sheet_name=tab_name)
        else:
            # If the sheet doesn't exist, create a new empty DataFrame
            chat_df = pd.DataFrame(columns=["Timestamp", "Sender", "Receiver", "Message"])
    except FileNotFoundError:
        # If the Excel file itself doesn't exist yet
        chat_df = pd.DataFrame(columns=["Timestamp", "Sender", "Receiver", "Message"])

    new_row = {
        "Timestamp": timestamp,
        "Sender": sender,
        "Receiver": receiver,
        "Message": message
    }
    chat_df = pd.concat([chat_df, pd.DataFrame([new_row])], ignore_index=True)

    with pd.ExcelWriter('datasheet.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        chat_df.to_excel(writer, sheet_name=tab_name, index=False)

    return jsonify({"status": "message sent"})


@app.route("/get_chats/<receiver>", methods=["GET"])
def get_chats(receiver):
    xls = pd.ExcelFile('datasheet.xlsx')
    sheet_names: List[str] = xls.sheet_names
    incoming_messages = []

    for sheet in sheet_names:
        if sheet.startswith("Chat_"):
            chat_df = pd.read_excel(xls, sheet_name=sheet)
            incoming = chat_df[chat_df["Receiver"] == receiver]
            incoming_messages.extend(incoming.to_dict(orient="records"))

    return jsonify(sorted(incoming_messages, key=lambda x: x["Timestamp"]))

if __name__ == '__main__':
    app.run(debug=True)
