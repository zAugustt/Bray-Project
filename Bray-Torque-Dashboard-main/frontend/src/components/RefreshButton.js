import React from 'react';
/**
 * Refresh Button Component
 * Renders a customizable back button.
 *
 * Props:
 * - onRefresh (function): a refresh function that gets triggered when the button is clicked
 */
const RefreshButton = ({ onRefresh }) => {
  return (
    <button className='refresh-btn' onClick={onRefresh}>
        Refresh
    </button>
  );
};

export default RefreshButton;
