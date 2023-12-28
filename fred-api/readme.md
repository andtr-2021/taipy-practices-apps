# FRED

`API Document`: https://fred.stlouisfed.org/docs/api/fred/#API 

`For this problem, we use the fred/series/observation endpoint`: 
> - https://fred.stlouisfed.org/docs/api/fred/series_observations.html#example_json 

**[Important]** 
`Definition of realtime_start and realtime_end:`
> - The real-time period marks when facts were true or when information was known until it changed. Economic data sources, releases, series, and observations are all assigned a real-time period. Sources, releases, and series can change their names, and observation data values can be revised. On almost all URLs, the default real-time period is today

### i. Get API Key:
- Register an account. 
- Request an API key.
    - Output: 10644614d71d570b8fb28c49378b7005 

### ii. Collected Data Format:
- ouput format: json
- converted format: csv
> date,value\
> 2000-01-01,169.3\
> 2000-02-01,170.0\
> 2000-03-01,171.0\
> 2000-04-01,170.9\
> 2000-05-01,171.2

### ii. Parameters in the API request:
- `realtime_start`: YYYY-MM-DD. The realtime-period will check if the data collected in the observation is true.
    - Default: today
- `realtime_end`: YYYY-MM-DD. The realtime-period will check if the data collected in the observation is true.
    - Default: today
- `observation_start`: YYYY-MM-DD. The actual date the value exists.
- `observation_end`: YYYY-MM-DD. The actual date the value exists.
- `frequency`: string. The frequency of the series. 
    - `Default`: all
    - `Options`: 
        - daily
        - weekly
        - monthly
        - quarterly
        - semiannual
        - annual
        - all
- `other parameters`: read about them more here - https://fred.stlouisfed.org/docs/api/fred/series_observations.html 

### iii. Insights:
- Each series will have a limit number of ranges such as daily, weekly, monthly, quarterly, semi-anually, and annual.
- When we call the series API, we will know the best ranges we can have for each series. For example with the GDP series, the best range we can get is quarterly.