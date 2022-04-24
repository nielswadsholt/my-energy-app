import { useEffect, useState } from 'react';
import './App.css';
import { getTimeSeries } from './server'
import { format, sub } from 'date-fns'
import { TimeSeries } from './models';

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
        ? <div className="App">
            <div>{timeSeries.resolution}</div>
            <div>{timeSeries.interval.start} - {timeSeries.interval.end}</div>
            {timeSeries.data_points.map(x => <div>{x.tick}: {x.value}</div>)}
        </div>
        : null
}

