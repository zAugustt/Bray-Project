import React, { useState, useEffect } from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import '../../styles/event-details.css';
import { useParams } from 'react-router-dom';

const AuxGraph = ({ auxData }) => {
    const { auxSensorID } = useParams();
    //const { data } = useAuxData(auxSensorID);

    const formattedData = auxData.map((dataPoint, index) => ({
      index,
      timestamp: dataPoint.timestamp,
      percentage: dataPoint.percentage / 1000.0, 
  }));

    const gradientOffset = () => {
      const dataMax = Math.max(...formattedData.map(i => i.percentage));
      const dataMin = Math.min(...formattedData.map(i => i.percentage));
    
      if (dataMax <= 0) return 0;
      if (dataMin >= 0) return 1;
      return dataMax / (dataMax - dataMin);
    }; 

    const xAxisTicks = formattedData.map((_, index) => index).filter(index => index % 1 === 0);

    const off = gradientOffset();

    return (
      <>
      <div className='download-button-container'>
      <h3 className='column-title'> Aux Sensor {auxSensorID} Signature Data</h3>
      
    </div>
      <ResponsiveContainer width="100%" height="90%">
              <AreaChart
                data={formattedData}
                margin={{
                  top: 10,
                  right: 30,
                  left: 15,
                  bottom: 15,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="index" ticks ={xAxisTicks}  label={{ value: 'Timestamp', position: 'insideBottom', offset: -10 }} />
                <YAxis  label={{ value: 'CO2 (%)', angle: -90, position: 'insideLeft' }} />
                <Tooltip 
                formatter={(value, name, props) => {
                  const { payload } = props;
                  return [`CO2: ${value}%\nTimestamp: ${payload.timestamp}`];
                }}
                labelFormatter={() => ''}
                />
                <defs>
                  <linearGradient id="splitColor" x1="0" y1="0" x2="0" y2="1">
                    <stop offset={off} stopColor="green" stopOpacity={1} />
                    <stop offset={off} stopColor="red" stopOpacity={1} />
                  </linearGradient>
                </defs>
                <Area
                  type="monotone"
                  dataKey="percentage"
                  stroke="#000"
                  fill="url(#splitColor)"
                />
              </AreaChart>
            </ResponsiveContainer>
            </>
    )
};

export default AuxGraph;