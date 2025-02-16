import React from 'react';
import Header from '../components/Header';
import SensorTable from '../components/sensor/SensorTable';
import '../styles/sensor.css';

const SensorPage = () => {
    return (
        <div>
            <Header />
            <SensorTable />
        </div>
    );
};

export default SensorPage;