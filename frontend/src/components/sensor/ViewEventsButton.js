// ButtonCellRenderer.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';

/**
 * ViewEventsButton Component
 * Renders button that redirects user to the events page associated with given sensor.
 * 
 * props:
 * - data: all information of the given event
 */
const ViewEventsButton = (props) => {
  const navigate = useNavigate();

  const handleClick = () => {
    // Redirect to /events with the selected row's data
    navigate(`/events/${props.data.id}`, { state: { rowData: props.data } });
  };

  return (
    <button className='view-details-btn' onClick={handleClick}>
      View Events
    </button>
  );
};

export default ViewEventsButton;
