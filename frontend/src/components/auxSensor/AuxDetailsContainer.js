import AuxGraph from "./AuxGraph";
import { useState, useEffect } from "react";
import { useNavigate, useParams } from 'react-router-dom';

const AuxDetailsContainer = () => {
    const { auxSensorID } = useParams();
    const [timestamp, setTimestamp] = useState('N/A');
    const navigate = useNavigate();

    /*useEffect(() => {
        if(sensorEvents.event_datas){
            setTimestamp(sensorEvents.event_datas[eventId-1].timestamp);
        }
        if(sensorData[sensorId-1]){
            setNumEvents(sensorData[sensorId - 1].numEvents);
        }
    }, [sensorEvents, sensorData, eventId]);*/

    const handleGoBack = () => {
        navigate(`/sensors`);
    }

    return(
        <div className='details-container'>
            <div className='sub-header-split-container'>
                <div className='left-column'>
                    <div className='details-sub-header-container'>
                        <button className="back-btn" onClick={handleGoBack}>
                            Back
                        </button>
                        <h3 className='details-event-name'>Aux Sensor {auxSensorID} - {timestamp}</h3>
                    </div>
                </div>
            </div>
            <div className='split-container'>
                <div className='column left-column'>
                    <AuxGraph />
                </div>
                <div className='column right-column'>
                    {/*<PacketInfo hidden={hidden}/>*/}
                </div>
            </div>
        </div>
    );
};

export default AuxDetailsContainer;