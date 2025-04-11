import AuxGraph from "./AuxGraph";
import { useState, useEffect } from "react";
import { useNavigate, useParams } from 'react-router-dom';
import { useAuxData } from "../../apiServices";

const AuxDetailsContainer = () => {
    const { auxSensorID } = useParams();
    const { auxData, refreshData } = useAuxData(auxSensorID);
    const [timestamp, setTimestamp] = useState('N/A');
    const navigate = useNavigate();

    useEffect(() => {
        setTimestamp(auxData.timestamp);
    }, [auxData]);

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