import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';

/**
 * Back Button Component
 * Renders a customizable back button.
 *
 * Props:
 * - target (string): The target destination, either the events page or sensors page.
 * - text (string): OPTIONAL string to add to the button (e.g. you can make button say "back to sensors").
 */
const BackButton = (props) => {
  const { sensorId } = useParams();
  const navigate = useNavigate();

  // Define handleClick based on props.data.target
  const handleClick = () => {
    if (props.target === 'events') {
      navigate(`/events/${sensorId}`);
    }
    if (props.target === 'sensors') {
      navigate(`/sensors`);
    }
  };

  return (
    <button className='back-btn' onClick={handleClick}>
      {`Back${props.text ? ` ${props.text}` : ''}`} 
    </button>
  );
};

export default BackButton;
