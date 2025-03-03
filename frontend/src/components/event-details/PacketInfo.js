import { useEffect, useState } from "react";
import { useEventDetails } from "../../apiServices";
import { useParams } from "react-router-dom";

/**
 * PacketInfo Component
 * Renders the PacketInfo container, showing information transmitted in the heartbeat record and event summary
 * 
 * props
 * - hidden: if true, the duplicated data won't be displayed
 */
const PacketInfo = (hidden) => {
    const { sensorId, eventId } = useParams();
    const { eventDetails, refreshData } = useEventDetails(sensorId, eventId, hidden);
    const [ displayedDetails, setDisplayedDetails] = useState({});
    const [ isStreaming, setIsStreaming ] = useState(false)
    const strokeTypes = {
        0: 'N/A',
        1: 'Open',
        2: 'Closed'
    };

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
        if(eventDetails){
            setIsStreaming(eventDetails.isStreaming);
            setDisplayedDetails(eventDetails);
        }
    }, [eventDetails])
    
    if (displayedDetails.torqueData) {
        displayedDetails.typeOfStroke = strokeTypes[displayedDetails.typeOfStroke] || displayedDetails.typeOfStroke;
    }
   
    return(
        <>
            <h3 className='column-title'> LoRa Event Data </h3>
            <div className='packet-content-container'>
                {Object.entries(displayedDetails).map(([key, value]) => 
                    key !== 'torqueData' ? (
                        <div className='attribute' key={key}>
                            <strong>{key}:</strong> {Array.isArray(value) ? value.join(', ') : String(value)}
                        </div>
                    ) : null
                )}
            </div>
        </>
    );
};

export default PacketInfo;