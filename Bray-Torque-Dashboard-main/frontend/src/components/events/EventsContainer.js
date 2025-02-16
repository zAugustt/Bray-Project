import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import EventTable from './EventTable';
import TrendGraph from './TrendGraph';
import { useSensorEvents } from '../../apiServices';
import '../../styles/events.css'

/**
 * EventsContainer Component
 * Renders the structure of the events page, holding EventsTable and TrendGraphs
 */
const EventsContainer = () => {
    const { sensorId } = useParams();
    const { sensorEvents, refreshData } = useSensorEvents(sensorId);
    const [isOpen, setIsOpen] = useState(false);
    const [batteryVoltages, setBatteryVoltages] = useState([]);
    const [maxTorques, setMaxTorques] = useState([]);
    const [strokeTimes, setStrokeTimes] = useState([]);
    const [temperatures, setTemperatures] = useState([]);
    const [loading, setLoading] = useState(true);

    const toggleSidebar = () => {
        setIsOpen(!isOpen);
    };

    useEffect(() => {
        if(sensorEvents.batteryVoltages){
            setBatteryVoltages(sensorEvents.batteryVoltages);
            setMaxTorques(sensorEvents.maxTorques);
            setStrokeTimes(sensorEvents.strokeTimes);
            setTemperatures(sensorEvents.temperatures);
            setLoading(false);
        }
    }, [sensorEvents]);

    return (
        <div>
            <div className={isOpen ? 'left-column-small' : ''}>
                <EventTable />
            </div>
            <div className={isOpen ? 'right-column-open' : ''}>
                <button className='openbtn' onClick={toggleSidebar} hidden={isOpen ? true : false}>
                    ☰
                </button>
                <div className='sidebar' hidden={isOpen ? false : true}>
                    <button className='closebtn' onClick={toggleSidebar}>
                    X
                    </button>
                    {loading ? (
                        <div className="loading">Loading data...</div>
                    ) : (
                        <div>
                            {/* add more trend graphs if needed */}
                            <TrendGraph title="Battery Voltage Data" dataKey="batteryVoltages" data={batteryVoltages} />
                            <TrendGraph title="Max Torque Data" dataKey="maxTorques" data={maxTorques} />
                            <TrendGraph title="Stroke Times Data" dataKey="strokeTimes" data={strokeTimes} />
                            <TrendGraph title="Temperature Data" dataKey="temperatures" data={temperatures} />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default EventsContainer;
