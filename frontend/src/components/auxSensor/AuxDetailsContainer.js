import AuxGraph from "./AuxGraph";
import { useState, useEffect } from "react";
import { useNavigate, useParams } from 'react-router-dom';
import { useAuxData } from "../../apiServices";
import RefreshButton from "../RefreshButton";

const AuxDetailsContainer = () => {
    const { auxSensorID } = useParams();
    const { auxData, refreshData } = useAuxData(auxSensorID);
    const [timestamp, setTimestamp] = useState('N/A');
    const navigate = useNavigate();

    useEffect(() => {
        if (auxData && auxData.length > 0) {
            setTimestamp(auxData[auxData.length - 1].timestamp); // Set the latest timestamp
        }
    }, [auxData]);

    const Refresh = () => {
        refreshData();
    }

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
                        <RefreshButton onRefresh={Refresh} />
                        <h3 className='details-event-name'>Aux Sensor {auxSensorID} - {timestamp}</h3>
                    </div>
                </div>
            </div>
            <div className='split-container'>
                <div className='column left-column'>
                    <AuxGraph auxData={auxData}/>
                </div>
            </div>
        </div>
    );
};

export default AuxDetailsContainer;