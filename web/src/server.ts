import { match } from 'ts-pattern'

export const getTimeSeries = (from_date: string, to_date: string, callback: (data: any) => void) => {
    const baseUrl = match(process.env.NODE_ENV)
        .with('development', _ => 'http://localhost:8000')
        .with('production', _ => 'TBD')
        .otherwise(_ => 'nothing to see here')

    fetch(`${baseUrl}/api/timeseries?${new URLSearchParams({
        from_date: from_date,
        to_date: to_date
    })}`, {
        mode: 'cors'
    })
        .then(response => response.json())
        .then(data => callback(data));
}