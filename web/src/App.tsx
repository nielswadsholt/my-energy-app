import { useEffect, useState } from 'react';
import './App.css';
import { getTimeSeries } from './server'
import { format, sub } from 'date-fns'
import { TimeSeries } from './models';
import { CartesianGrid, Line, LineChart, Tooltip, XAxis, YAxis } from 'recharts'

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

    return timeSeries
        ? <div className='App'>
            <div>{timeSeries.resolution}</div>
            <div>{timeSeries.interval.start} - {timeSeries.interval.end}</div>
            <LineChart
                width={1200}
                height={800}
                data={timeSeries.data_points}
                margin={{ top: 5, right: 20, left: 10, bottom: 5 }} >
                    <XAxis dataKey='tick' />
                    <YAxis dataKey='value'/>
                    <Tooltip/>
                    <CartesianGrid stroke='#f5f5f5' />
                    <Line type='monotone' dataKey='value' stroke='#ff7300' />
            </LineChart>
        </div>
        : null
}

