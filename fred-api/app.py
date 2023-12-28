"""
- Visualize economic data. 
- Able to set the start_date and end_date. 
- Able to chage data ranges such as quarterly, monthly, weekly, daily, etc.
- Able to zoom in and out.
"""

from taipy.gui import Gui

startdate = "2000-01-01"
enddate = "2023-07-01"
rangeselector = ["daily", "weekly", "monthly", "quarterly", "semiannual", "annual"]
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

|>

<|layout|columns= 1|
<h2> Gross Domestic Product (GDP) </h2>
<|{data}|chart|x=x_col|y=y_col1|>>
|>
|>

"""

Gui(page).run(dark_mode=False)

