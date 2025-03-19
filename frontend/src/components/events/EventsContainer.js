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
    const [loading, setLoading] = useState(true);

    const toggleSidebar = () => {
        setIsOpen(!isOpen);
    };

    useEffect(() => {
        if(sensorEvents.batteryVoltages){
            setBatteryVoltages(sensorEvents.batteryVoltages);
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
                            <TrendGraph title="Carbon Dioxide Data" dataKey="batteryVoltages" data={batteryVoltages} />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default EventsContainer;
