import React, { useEffect, useRef } from 'react';
import { AgCharts } from 'ag-charts-community'; // Ensure ag-charts-community is installed

/**
 * TrendGraph Component
 * Renders a graph that graphs the given data (showing historical trends of a event property)
 * 
 * props:
 * - title: title of the graph
 * - dataKey: property being graphed
 * - data: data points being graphed 
 */
const TrendGraph = ({ title, dataKey, data }) => {
  const chartRef = useRef(null);
  const units = {
    maxTorques: 'µV',
    strokeTimes: 'ms',
    batteryVoltages: 'mv',
    temperatures: 'C'
  };
  const tooltipLabels = {
    maxTorques: 'Maximum Torque',
    strokeTimes: 'Stroke Time',
    batteryVoltages: 'Battery Voltage',
    temperatures: 'Temperature'
  };
  const unit = units[dataKey] || '';
  const tooltipLabel = tooltipLabels[dataKey] || '';

  useEffect(() => {
    // Tooltip configuration
    const tooltip = {
      renderer: ({ datum, yKey }) => {
        return {
          content: `${tooltipLabel}: ${datum[yKey]} ${unit}`,
        };
      },
    };

    // Prepare the data for charting
    const chartData = data.map((value, index) => ({
      index: index + 1,
      value,
    }));

    // Chart options
    const options = {
      container: chartRef.current,
      data: chartData,
      title: {
        text: title || `${dataKey} Data Chart`,
      },
      series: [
        {
          type: 'line', // Change to 'line' for a clearer plot of individual values
          xKey: 'index',
          yKey: 'value',
          tooltip,
          marker: {
            enabled: true,
          },
        },
      ],
      axes: [
        {
          type: 'category', // X-axis as category for index
          position: 'bottom',
          title: { text: 'Events' },
        },
        {
          type: 'number', // Y-axis for values
          position: 'left',
          title: { text: `${dataKey} (${unit})` },
        },
      ],
    };

    // Create the chart
    AgCharts.create(options);

    // Cleanup function to destroy the chart when the component unmounts
    return () => {
      if (chartRef.current) {
        chartRef.current.innerHTML = ''; // Clear chart container
      }
    };
  }, [data, dataKey, title]);

  return (
    <div>
      <div className='trend-graph' id='myChart' ref={chartRef}></div>
    </div>
  );
};

export default TrendGraph;
