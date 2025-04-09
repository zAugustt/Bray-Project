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
    if(props.data.devEUI) {
      navigate(`/events/${props.data.id}`, { state: { rowData: props.data } });
    } else {
      navigate(`/aux_sensors/${props.data.id}`, { state: props.data })
    }
    
  };

  if(props.data.devEUI) {
    return (
      <button className='view-details-btn' onClick={handleClick}>
        View Events
      </button>
    );
  } else {
    return (
      <button className='view-details-btn' onClick={handleClick}>
      View Data
    </button>
    );
  }
  
};

export default ViewEventsButton;
