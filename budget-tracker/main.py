from taipy.gui import Gui, navigate, notify
import pandas as pd
import json


# File path for the JSON file
json_file_path = "spendings.json"

categories = ["Housing", "Transportation", "Food", "Ultilities", "Insurance", "Medical & Healthcare", "Saving, Investing, & Debt Payments", "Personal Spending", "Recreation & Entertainment", "Miscellaneous"]

root_md="<|menu|label=Menu|lov={[('Information', 'Information'), ('Spending', 'Spending'), ('Details', 'Details')]}|on_action=on_menu|>"

class Spending:
    def __init__(self, id, value, category):
        self.id, self.value, self.category = (id, value, category)

# Check if the JSON file exists and create it if it doesn't
try:
    with open(json_file_path, "x") as file:
        json.dump([], file)
except FileExistsError:
    pass

# Function to load spendings from JSON file
def load_spendings():
    with open(json_file_path, "r") as file:
        return [Spending(**data) for data in json.load(file)]

# Load spendings
spendings = load_spendings()


budget = 0
income = 0
information_md="""
## Your information

Budget
<|{budget}|number|>

Income
<|{income}|number|>
"""

 
value = 0
category = categories[2]
spending_md="""
## Your spending information

Value
<|{value}|number|>

Type
# <|{category}|selector|lov={categories}|dropdown|>

<|Confirm|button|on_action=on_confirm_button_action|>
"""

def on_confirm_button_action(state):
    global spendings
    if(state.value == 0):
        notify(state, 'error', f'Please insert a value')
        return
        
    new_spending = Spending(len(spendings), state.value, state.category)
    spendings.append(new_spending)
    # Update JSON file
    with open(json_file_path, "w") as file:
        json.dump([vars(spending) for spending in spendings], file)


# Update DataFrame creation
dataframe = pd.DataFrame.from_records([vars(spending) for spending in spendings])
details_md="""
## Spending details
<|{dataframe}|table|>
<|{dataframe}|chart|type=pie|values=value|labels=category|>
"""

# def on_change(state, var, val):
#     if var == "value":
#         state.value = val
#     elif var == "category":
#         state.category = val

def on_menu(state, action, info):
    page = info["args"][0]
    navigate(state, to=page)
    if page == "Details":
        # Reload spendings from the JSON file
        spendings = load_spendings()
        # Update DataFrame and assign to state
        dataframe = pd.DataFrame.from_records([vars(spending) for spending in spendings])
        state.dataframe = dataframe

pages = {
    "/": root_md,
    "Information": information_md,
    "Spending": spending_md,
    "Details": details_md
}

Gui(pages=pages).run()
