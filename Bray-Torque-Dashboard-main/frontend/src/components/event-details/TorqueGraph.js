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
import { useEventDetails } from '../../apiServices';
import DownloadButton from './DownloadButton';

/**
 * separateDataIntoPackets Function
 * Separates the eventDetails data into individual packets
 * 
 * props
 * - eventDetails: all event information
 */
export const separateDataIntoPackets = (eventDetails) => {
  const packetArray = [];
  let startIndex = 0;

  for (let i = 0; i < eventDetails.recordLengths.length; ++i) {
    const packetLength = eventDetails.recordLengths[i];

    if (startIndex + packetLength > eventDetails.torqueData.length) {
      throw new Error("Invalid packet length: exceeds torqueData length.");
    }

    for (let j = startIndex; j < startIndex + packetLength; ++j) {
      packetArray.push({ index: j, torque: eventDetails.torqueData[j] });
    }

    startIndex += packetLength;
  }

  return packetArray;
};

/**
 * TorqueGraph Component
 * Renders the TorqueGraph, displaying the torque data transmitted in the event
 * 
 * props
 * - hidden: if true, the duplicated data won't be displayed
 */
const TorqueGraph = (hidden) => {
  const { sensorId, eventId } = useParams();
  const { eventDetails, refreshData } = useEventDetails(sensorId, eventId, hidden);
  const [ strokeType, setStrokeType ] = useState("Close");
  const [ torqueData, setTorqueData ] = useState([]);
  const [ isStreaming, setIsStreaming ] = useState(false)

  useEffect(() => {
    let intervalId;

    if (isStreaming) {
        intervalId = setInterval(() => {
            refreshData();
        }, 5000);
    }

    return () => {
        if (intervalId) clearInterval(intervalId);
    };
  }, [isStreaming, refreshData]);

  useEffect(() => {
    if (eventDetails){
      setIsStreaming(eventDetails.isStreaming);
      if (eventDetails.torqueData && eventDetails.recordLengths) {
        setStrokeType(eventDetails.typeOfStroke === 1 ? "Open" : "Close");
        const packets = separateDataIntoPackets(eventDetails);
        setTorqueData(packets);
      }
    }
  }, [eventDetails]);

  useEffect(() => {
    refreshData();
  }, [hidden])

  // Calculate the gradient offset based on torque data
  const gradientOffset = () => {
    const dataMax = Math.max(...torqueData.map(i => i.torque));
    const dataMin = Math.min(...torqueData.map(i => i.torque));

    if (dataMax <= 0) return 0;
    if (dataMin >= 0) return 1;
    return dataMax / (dataMax - dataMin);
  };

  const xAxisTicks = torqueData.map((_, index) => index).filter(index => index % 5 === 0);
  
  const off = gradientOffset();

  return (
    <>
    <div className='download-button-container'>
      {isStreaming ? (
        <h3 className='column-title'> Torque Signature Data - Receiving... </h3>
      ) : (
        <>
          <h3 className='column-title'> Torque Signature Data - {strokeType} </h3>
          <DownloadButton hidden={hidden}/>
        </>
      )}
    </div>
      <ResponsiveContainer width="100%" height="90%">
        <AreaChart
          data={torqueData}
          margin={{
            top: 10,
            right: 30,
            left: 15,
            bottom: 15,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="index" ticks ={xAxisTicks}  label={{ value: 'Data Points', position: 'insideBottom', offset: -10 }} />
          <YAxis  label={{ value: 'Torque (µV)', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
          <defs>
            <linearGradient id="splitColor" x1="0" y1="0" x2="0" y2="1">
              <stop offset={off} stopColor="green" stopOpacity={1} />
              <stop offset={off} stopColor="red" stopOpacity={1} />
            </linearGradient>
          </defs>
          <Area
            type="monotone"
            dataKey="torque"
            stroke="#000"
            fill="url(#splitColor)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </>
  );
};

export default TorqueGraph;
