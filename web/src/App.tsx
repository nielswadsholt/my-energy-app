import { useEffect, useState } from 'react';
import './App.css';
import { getTimeSeries } from './server'
import { format, sub } from 'date-fns'
import { TimeSeries } from './models';
import { VictoryChart, VictoryGroup, VictoryLine, VictoryScatter, VictoryTooltip, VictoryVoronoiContainer } from 'victory'

export const App = () => {
    const [timeSeries, setTimeSeries] = useState<TimeSeries>();

    useEffect(() => {
        const to_date = new Date();
        const from_date = sub(to_date, { days: 2 });

        getTimeSeries(
            format(from_date, 'yyyy-MM-dd'),
            format(to_date, 'yyyy-MM-dd'),
            (data) => {
                setTimeSeries(data)
            }
        )
    }, []);

    console.log(timeSeries?.data_points)

    return timeSeries
        ? <div className='App'>
            <div>{timeSeries.resolution}</div>
            <div>{timeSeries.interval.start} - {timeSeries.interval.end}</div>
            <VictoryChart containerComponent={<VictoryVoronoiContainer/>} >
                <VictoryGroup
                    color="#c43a31"
                    data={timeSeries.data_points.map(p => ({ x: p.tick, y: p.value }))}
                    labels={({ datum }) => `y: ${datum.y}`}
                    labelComponent={
                        <VictoryTooltip
                            style={{ fontSize: 8 }}
                        />
                    }
                >
                    <VictoryLine />
                    <VictoryScatter
                        size={({ active }) => active ? 8 : 3}
                    />
                </VictoryGroup>
            </VictoryChart>
        </div>
        : null
}

