# FRED

API Document: https://fred.stlouisfed.org/docs/api/fred/#API 

For this problem, we use the observation endpoint: 
> - https://fred.stlouisfed.org/docs/api/fred/series_observations.html#example_json 

**Definition of realtime_start and realtime_end:** 
> - The real-time period marks when facts were true or when information was known until it changed. Economic data sources, releases, series, and observations are all assigned a real-time period. Sources, releases, and series can change their names, and observation data values can be revised. On almost all URLs, the default real-time period is today

1. Get API Key:
- Register an account. 
- Request an API key.
    - Output: 10644614d71d570b8fb28c49378b7005 