import TorqueGraph from './TorqueGraph';
import PacketInfo from './PacketInfo';
import BackButton from '../BackButton';
import DownloadButton from './DownloadButton';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import '../../styles/event-details.css'
import { useSensorData, useSensorEvents } from '../../apiServices';
import { useState, useEffect } from 'react';

/**
 * DetailsContainer Component
 * Renders the event-details page with information of selected event (useParams), holding TorqueGraph and PacketInfo
 */
const DetailsContainer = () => {
    const { sensorId, eventId } = useParams();
    const [timestamp, setTimestamp] = useState('N/A');
    const [numEvents, setNumEvents] = useState(1);
    const [hidden, setHidden] = useState(true);
    const sensorEvents = useSensorEvents(sensorId).sensorEvents;
    const sensorData = useSensorData().sensorData;
    const navigate = useNavigate();

    const prevEvent = () => {
        if(Number(eventId) !== 1){
            navigate(`/events/${sensorId}/event-details/${Number(eventId) - 1}`);
        }
    }

    const nextEvent = () => {
        if(Number(eventId) !== numEvents){
            navigate(`/events/${sensorId}/event-details/${Number(eventId) + 1}`);
        }
    }

    const toggleHidden = () => {
        setHidden(!hidden);
    }

    useEffect(() => {
        if(sensorEvents.event_datas){
            setTimestamp(sensorEvents.event_datas[eventId-1].timestamp);
        }
        if(sensorData[sensorId-1]){
            setNumEvents(sensorData[sensorId - 1].numEvents);
        }
    }, [sensorEvents, sensorData, eventId]);

    return(
        <div className='details-container'>
            <div className='sub-header-split-container'>
                <div className='left-column'>
                    <div className='details-sub-header-container'>
                        <BackButton target='events' />
                        <h3 className='details-event-name'>Sensor {sensorId}, Event {eventId} - {timestamp}</h3>
                        <label className="switch">
                            Show Hidden Data: 
                            <input type="checkbox" onChange={toggleHidden} defaultChecked={false}></input>
                            <span className="slider"></span>
                        </label>
                    </div>
                </div>
                <div className='right-column packet-btn-container'>
                    <button className='packet-btn' onClick={prevEvent}> Prev </button>
                    <button className='packet-btn' onClick={nextEvent}> Next </button>
                </div>
            </div>
            <div className='split-container'>
                <div className='column left-column'>
                    <TorqueGraph hidden={hidden} />
                </div>
                <div className='column right-column'>
                    <PacketInfo hidden={hidden}/>
                </div>
            </div>
        </div>
    );
};

export default DetailsContainer;