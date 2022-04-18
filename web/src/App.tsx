import { useEffect, useState } from 'react';
import './App.css';
import { getTimeSeries } from './server'
import { format, sub } from 'date-fns'

export const App = () => {
    const [timeSeries, setTimeSeries] = useState('');

    useEffect(() => {
        const to_date = new Date();
        const from_date = sub(to_date, { days: 1 });

        getTimeSeries(
            format(from_date, 'yyyy-MM-dd'),
            format(to_date, 'yyyy-MM-dd'),
            (data) => setTimeSeries(JSON.stringify(data))
        )
    }, []);

    return <div className="App">
        {timeSeries}
    </div>
}

