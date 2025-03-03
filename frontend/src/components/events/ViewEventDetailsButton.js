import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';

/**
 * ViewEventDetailsButton Component
 * Renders button that redirects user to the events-details page associated with given event.
 * 
 * props:
 * - data: information of the selected event
 */
const ViewEventDetailsButton = (props) => {
    const { sensorId } = useParams();
    const navigate = useNavigate();

    const handleClick = () => {
        // Redirect to /events-details with the selected row's data
        navigate(`/events/${sensorId}/event-details/${props.data.id}`);
    };

    return (
        <button className='view-details-btn' onClick={handleClick}>
            View Details
        </button>
    );
};

export default ViewEventDetailsButton;
