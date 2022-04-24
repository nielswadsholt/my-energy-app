from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from eloverblik_client import EloverblikClient
from config_handler import read_from_config
from models.time_series import TimeSeries

__eloverblik_client = EloverblikClient()

app = FastAPI(title='My Energy App')

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

date_param = Query(None, description= 'Format: \'YYYY-MM-DD\'')

@app.get("/api/timeseries/")
def get_timeseries(from_date: str = date_param, to_date: str = date_param):
    metering_point_id = read_from_config('meteringpointid')
    aggr = 'Hour'
    raw_time_series = __eloverblik_client.get_time_series(metering_point_id, from_date, to_date, aggr)
    time_series = TimeSeries.from_raw_data(raw_time_series)

    return time_series