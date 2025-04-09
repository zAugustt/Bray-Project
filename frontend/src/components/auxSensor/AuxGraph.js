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

const fakeData = [0.00, 5.25, 10.33, 30.55, 80.99, 45.22, 62.77, 65.21, 82.47, 74.33];

const formattedData = fakeData.map((value, index) => ({
  index,
  ppm: value,
}));

const gradientOffset = () => {
  const dataMax = Math.max(...formattedData.map(i => i.ppm));
  const dataMin = Math.min(...formattedData.map(i => i.ppm));

  if (dataMax <= 0) return 0;
  if (dataMin >= 0) return 1;
  return dataMax / (dataMax - dataMin);
};

const xAxisTicks = formattedData.map((_, index) => index).filter(index => index % 1 === 0);;

const off = gradientOffset();

const AuxGraph = () => {
    const { auxSensorID } = useParams();
    //const { sensorData, setSensorData } = 
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
                <XAxis dataKey="index" ticks ={xAxisTicks}  label={{ value: 'Data Points', position: 'insideBottom', offset: -10 }} />
                <YAxis  label={{ value: 'CO2 (ppm)', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <defs>
                  <linearGradient id="splitColor" x1="0" y1="0" x2="0" y2="1">
                    <stop offset={off} stopColor="green" stopOpacity={1} />
                    <stop offset={off} stopColor="red" stopOpacity={1} />
                  </linearGradient>
                </defs>
                <Area
                  type="monotone"
                  dataKey="ppm"
                  stroke="#000"
                  fill="url(#splitColor)"
                />
              </AreaChart>
            </ResponsiveContainer>
            </>
    )
};

export default AuxGraph;