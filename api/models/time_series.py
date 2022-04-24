from pydantic import BaseModel

class Interval(BaseModel):
    start: str
    end: str

class DataPoint:
    tick: int
    value: float

    def __init__(self, raw_data: str) -> None:
        self.tick = int(raw_data['position'])
        self.value = float(raw_data['out_Quantity.quantity'])

class TimeSeries:
    resolution: str
    interval: Interval
    data_points: list[DataPoint]

    def __init__(self, resolution: str, interval: Interval, data_points: list[DataPoint]) -> None:
        self.resolution = resolution
        self.interval = interval
        self.data_points = data_points

    @classmethod
    def from_raw_data(cls, raw_data: str):
        raw_series = raw_data['result'][0]['MyEnergyData_MarketDocument']['TimeSeries'][0]
        first_period = raw_series['Period'][0]
        resolution = first_period['resolution']
        interval = first_period['timeInterval']
        data_points = first_period['Point']
        time_series = TimeSeries(resolution, Interval(**interval), [DataPoint(p) for p in data_points])

        return time_series
