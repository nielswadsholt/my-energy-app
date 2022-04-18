from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from eloverblik_client import EloverblikClient
from config_handler import read_from_config

__eloverblik_client = EloverblikClient()

app = FastAPI()

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

@app.get("/api/timeseries/")
def get_timeseries(from_date: str, to_date: str):
    metering_point_id = read_from_config('meteringpointid')
    aggr = 'Hour'

    return __eloverblik_client.get_time_series(metering_point_id, from_date, to_date, aggr)