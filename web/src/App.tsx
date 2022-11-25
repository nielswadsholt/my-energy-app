import { CSSProperties, useEffect, useState } from 'react';
import './App.css';
import { getTimeSeries } from './server'
import { add, format, sub } from 'date-fns'
import { TimeSeries } from './models';
import { VictoryAxis, VictoryBar, VictoryChart, VictoryTheme, VictoryTooltip, VictoryVoronoiContainer } from 'victory'
import da from 'date-fns/esm/locale/da/index.js';
import _ from 'lodash';
import { match, P } from 'ts-pattern';

export const App = () => {
    const [timeSeries, setTimeSeries] = useState<TimeSeries>();
    const [toDate, setToDate] = useState<Date>(new Date());

    useEffect(() => {
        const fromDate = sub(toDate, { days: 2 });

        getTimeSeries(
            format(fromDate, 'yyyy-MM-dd'),
            format(toDate, 'yyyy-MM-dd'),
            (data) => {
                setTimeSeries(data)
            }
        )
    }, [toDate]);

    const buttonStyles : CSSProperties = {
        background: 'initial',
        border: 'initial',
        margin: '0 5px'
    }

    return timeSeries
        ? <div className='App'>
            <h1>Mit energiforbrug</h1>
            <div>
                <button style={buttonStyles} onClick={() => setToDate(sub(toDate, { days: 1 }))}>{'<'}</button>
                <span style={{ padding: '0 10px' }}>{_.upperFirst(format(new Date(timeSeries.interval.start), "EEEE 'den' dd MMMM yyyy", { locale: da }))}</span>
                <button style={buttonStyles} onClick={() => setToDate(add(toDate, { days: 1 }))}>{'>'}</button>
            </div>
            <VictoryChart
                containerComponent={<VictoryVoronoiContainer/>}
                height={200}
                theme={VictoryTheme.material}
            >
                <VictoryBar
                    barRatio={0.6}
                    cornerRadius={2.5}
                    data={timeSeries.data_points.map(p => ({ x: p.tick, y: p.value }))}
                    labels={({ datum }) => `${datum.y} kWh`}
                    labelComponent={
                        <VictoryTooltip
                            flyoutStyle={{
                                strokeWidth: 0.1
                            }}
                            style={{
                                fontFamily: 'Courier New',
                                fontSize: 6
                            }}
                            cornerRadius={2}
                        />
                    }
                    style={{ data: { fill: ({ datum }) => match(datum)
                        .with({ y: P.when(y => y as number > 0.20) }, () => "#c43a31")
                        .with({ y: P.when(y => y as number > 0.10) }, () => "#C48731")
                        .otherwise(() => '#9DC431')
                    }}}
                />
                <VictoryAxis
                    crossAxis
                    fixLabelOverlap={false}
                    style={{
                        tickLabels: {
                            fontSize: 8
                        }
                    }}
                />
                <VictoryAxis
                    dependentAxis
                    label='kWh'
                    style={{
                        axisLabel: {
                            fontSize: 8,
                            padding: 35
                        },
                        tickLabels: {
                            fontSize: 8
                        }
                    }}
                />
            </VictoryChart>
        </div>
        : null
}

