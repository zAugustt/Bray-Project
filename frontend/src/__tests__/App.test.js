import { render, screen } from '@testing-library/react';
import App from '../App';
import { BrowserRouter } from 'react-router-dom';

describe('App Routing', () => {
  it('should render SensorPage when navigating to "/"', () => {
    render(
        <App />
    );
    expect(screen.getByText('Refresh')).toBeInTheDocument(); // Adjust with actual text from SensorPage
  });

  it('should render EventPage when navigating to "/events/:sensorId"', () => {
    render(
        <App />
    );
    window.history.pushState({}, 'Test', '/events/123'); // Simulate navigation to /events/123
    expect(screen.getByText('Refresh')).toBeInTheDocument(); // Adjust with actual text from EventPage
  });

  it('should render EventDetailsPage when navigating to "/events/:sensorId/event-details/:eventId"', () => {
    render(
        <App />
    );
    window.history.pushState({}, 'Test', '/events/123/event-details/456'); // Simulate navigation to /events/123/event-details/456
    expect(screen.getByText('Refresh')).toBeInTheDocument(); // Adjust with actual text from EventDetailsPage
  });
});
