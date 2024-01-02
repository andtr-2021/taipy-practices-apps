"""
- Visualize economic data. 
- Able to set the start_date and end_date. 
- Able to chage data ranges such as quarterly, monthly, weekly, daily, etc.
- Able to zoom in and out.
"""

from taipy.gui import Gui
import requests
import pandas as pd

# SCRAPE data from FRED when the app is loaded
api_key = '10644614d71d570b8fb28c49378b7005'
base_url = 'https://api.stlouisfed.org/fred/'
obs_endpoint = 'series/observations'

# Assign parameters
series_id = 'GDP'
start_date = '2000-01-01'
end_date = '2023-07-01'
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
    obs_data = pd.DataFrame(res_data['observations'])
    obs_data['date'] = pd.to_datetime(obs_data['date'])
    if obs_data['value'].dtype == object:
        try :
            obs_data['value'] = obs_data['value'].astype(float)
        except ValueError:
            print('Failed to convert to float')
    elif obs_data['value'].dtype == float:
        pass
else:
    print('Failed to retrieve data. Status code:', response.status_code)

# create a pandas dataframe
print("Initial Data:")
print(obs_data.head())
# create a dict for chart data
chart_data = { "Date": obs_data['date'], "Values": obs_data['value'] }

# filter variables
startdate = "2000-01-01"
enddate = "2023-07-01"
frequency_list = ["Daily", "Weekly", "Monthly", "Quarterly", "Semiannual", "Annual"]
chosen_frequency = "Quarterly"

# Plot multiple series on a same chart 
series_list = ["CPIAUCSL", "NIKKEI225", "PCU2122212122210", "APU0000708111"]

final_data = pd.DataFrame()

a = 1 

# collect data 
for i in series_list:
    series_id = i 
    start_date = '2000-01-01'
    end_date = '2023-07-01'
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
        obs_data = pd.DataFrame(res_data['observations'])
        obs_data['date'] = pd.to_datetime(obs_data['date'])
        if obs_data['value'].dtype == object:
            try :
                obs_data['value'] = obs_data['value'].astype(float)
            except ValueError:
                print('Failed to convert to float')
        elif obs_data['value'].dtype == float:
            pass
    else:
        print('Failed to retrieve data. Status code:', response.status_code)

    # create a pandas dataframe
    print("Initial Data:")
    print(obs_data.head())
    # create a dict for chart data
    chart_data = { "Date": obs_data['date'], "Values": obs_data['value'] }

    if a == 1:
        # get the date columns 
        final_data['Date'] = obs_data['date']
        final_data[i] = obs_data['value']
        a += 1 
    else: 
        # get the value columns 
        final_data[i] = obs_data['value']

print(final_data.head())    

multiple_line_chart_date = { "Date": final_data['Date'], "CPIAUCSL": final_data['CPIAUCSL'], "NIKKEI225": final_data['NIKKEI225'] }

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
Frequency Ranges: <|{chosen_frequency}|>
<|{chosen_frequency}|selector|lov={frequency_list}|dropdown|>

<|Apply|button|on_action=data_collection|>
|>

<|layout|columns= 1|
<h2> GDP Chart </h2>
<|{chart_data}|chart|mode=lines|x=Date|y=Values|>

<br></br>

<|{final_data}|chart|mode=lines|x=Date|y[1]=CPIAUCSL|y[2]=PCU2122212122210|y[3]=APU0000708111|>
|>
|>

"""

def data_collection(state):
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
        obs_data = pd.DataFrame(res_data['observations'])
        obs_data['date'] = pd.to_datetime(obs_data['date'])
        if obs_data['value'].dtype == object:
            try :
                obs_data['value'] = obs_data['value'].astype(float)
            except ValueError:
                print('Failed to convert to float')
        elif obs_data['value'].dtype == float:
            pass
    else:
        print('Failed to retrieve data. Status code:', response.status_code)

    # create a pandas dataframe
    print("Updated Data:")
    print(obs_data.head())
    # create a dict for chart data
    state.chart_data = { "Date": obs_data['date'], "Values": obs_data['value'] }

Gui(page).run(dark_mode=False)

