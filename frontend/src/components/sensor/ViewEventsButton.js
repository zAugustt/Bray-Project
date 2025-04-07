// ButtonCellRenderer.jsx
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
    if(props.data.auxSensorID) {
      navigate(`/aux_sensors/${props.data.auxSensorID}`, { state: props.data })
    } else {
      navigate(`/events/${props.data.id}`, { state: { rowData: props.data } });
    }
    
  };

  if(props.data.auxSensorID) {
    return (
      <button className='view-details-btn' onClick={handleClick}>
        View Data
      </button>
    );
  } else {
    return (
      <button className='view-details-btn' onClick={handleClick}>
        View Events
      </button>
    );
  }
  
};

export default ViewEventsButton;
