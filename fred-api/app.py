"""
- Visualize economic data. 
- Able to set the start_date and end_date. 
- Able to chage data ranges such as quarterly, monthly, weekly, daily, etc.
- Able to zoom in and out.
"""

from taipy.gui import Gui

startdate = "2000-01-01"
enddate = "2023-07-01"
rangeselector = ["quarterly", "semiannual", "annual"]
daterange = "quarterly"

data = {"x_col":[0,1,2], "y_col1":[4,1,2]}

page = """

<center><h1> FRED Macro Economic Data </h1></center>

<|layout|columns=50px 300px 1000px|

<|layout|columns= 1|

|>

<|layout|columns= 1|
<h2> Filter </h2>

Date Start:
<|{startdate}|date|>
<br></br>
Date End:
<|{enddate}|date|>
<br></br>
Date Range: <|{daterange}|>
<|{daterange}|selector|lov={rangeselector}|>

<|Apply|button|on_action=data_collection|>
|>

<|layout|columns= 1|
<h2> Gross Domestic Product (GDP) </h2>
<|{data}|chart|x=x_col|y=y_col1|>>
|>
|>

"""

import requests
import pandas as pd

api_key = '10644614d71d570b8fb28c49378b7005'

# Define the FRED API endpoint
base_url = 'https://api.stlouisfed.org/fred/'

# Assign endpoint
obs_endpoint = 'series/observations'



def data_collection(state):
    print(state.startdate)
    print(state.enddate)
    print(state.daterange)

    # Assign parameters
    series_id = 'GDP'
    start_date = state.startdate
    end_date = state.enddate
    ts_frequency = 'q'

    obs_params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': ts_frequency
    }

    response = requests.get(base_url + obs_endpoint, params=obs_params)

    if response.status_code == 200:
        res_data = response.json()
        print(res_data.keys())
        obs_data = pd.DataFrame(res_data['observations'])
        obs_data['date'] = pd.to_datetime(obs_data['date'])
        obs_data.set_index('date', inplace=True)
        if obs_data['value'].dtype == object:
            print('Converting to numeric')
        elif obs_data['value'].dtype == float:
            pass
    else:
        print('Failed to retrieve data. Status code:', response.status_code)

    print(obs_data.head())

    state.date.x_col = obs_data['date']
    state.date.y_col1 = obs_data['value']

    print(state.date.x_col)
    print(state.date.y_col1)

Gui(page).run(dark_mode=False)

