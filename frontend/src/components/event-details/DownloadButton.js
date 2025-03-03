import React from "react";
import { useEventDetailsDownload } from "../../apiServices";
import { useParams } from "react-router-dom";
import '../../styles/event-details.css'

/**
 * DownloadButton Component
 * Renders a download button that allows user to download a csv of the event's details
 */
const DownloadButton = ({hidden}) => {
    const { sensorId, eventId } = useParams();
    const { eventDetails } = useEventDetailsDownload(sensorId, eventId, hidden);

    const downloadCSV = () => {
        if (eventDetails) {
            const url = window.URL.createObjectURL(eventDetails);
            const link = document.createElement("a");
            link.href = url;
            link.download = `event_${sensorId}_${eventId}.csv`;

            document.body.appendChild(link);
            link.click();

            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        } else {
            console.error("No event details available for download.");
        }
    };

    return (
        <div>
            <button className='packet-btn' onClick={downloadCSV}>Download CSV</button>
        </div>
    );
};

export default DownloadButton;
