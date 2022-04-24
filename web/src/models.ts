export type Interval = {
    start: string
    end: string
}

export type DataPoint = {
    tick: number
    value: number
}

export type TimeSeries = {
    resolution: string
    interval: Interval
    data_points: DataPoint[]
}