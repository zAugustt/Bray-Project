import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import EventsContainer from '../EventsContainer';
import '@testing-library/jest-dom';
import { useParams } from 'react-router-dom';
import { useSensorEvents } from '../../../apiServices';

// Mock dependencies
jest.mock('react-router-dom', () => ({
  useParams: jest.fn(),
}));

jest.mock('../../../apiServices', () => ({
  useSensorEvents: jest.fn(),
}));

jest.mock('../EventTable', () => () => <div>Mock EventTable</div>);
jest.mock('../TrendGraph', () => ({ title, dataKey, data }) => (
  <div>{`${title} - ${dataKey} - ${data}`}</div>
));

describe('EventsContainer', () => {
  const mockSensorId = '123';
  const mockSensorEvents = {
    batteryVoltages: [1.5, 1.6, 1.7],
    maxTorques: [10, 20, 30],
    strokeTimes: [100, 200, 300],
    temperatures: [22, 23, 24],
  };

  beforeEach(() => {
    useParams.mockReturnValue({ sensorId: mockSensorId });
    useSensorEvents.mockReturnValue({
      sensorEvents: mockSensorEvents,
      refreshData: jest.fn(),
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders loading state initially', () => {
    // Use a fresh set of data for each test to avoid cross-test pollution
    useSensorEvents.mockReturnValueOnce({ sensorEvents: {}, refreshData: jest.fn() });

    render(<EventsContainer />);

    expect(screen.getByText('Loading data...')).toBeInTheDocument();
  });

  it('displays the EventTable and TrendGraph components with correct data after loading', async () => {
    render(<EventsContainer />);

    // Check for EventTable rendering
    expect(screen.getByText('Mock EventTable')).toBeInTheDocument();

    // Verify that TrendGraph components render with the correct data
    await waitFor(() => {
      expect(screen.getByText('Battery Voltage Data - batteryVoltages - 1.5,1.6,1.7')).toBeInTheDocument();
      expect(screen.getByText('Max Torque Data - maxTorques - 10,20,30')).toBeInTheDocument();
      expect(screen.getByText('Stroke Times Data - strokeTimes - 100,200,300')).toBeInTheDocument();
      expect(screen.getByText('Temperature Data - temperatures - 22,23,24')).toBeInTheDocument();
    });
  });

  it('toggles sidebar visibility when buttons are clicked', async () => {
    render(<EventsContainer />);

    // Sidebar is hidden initially; open button should be visible
    const openButton = screen.getByText('☰');
    expect(openButton).toBeVisible();

    // Click open button to show sidebar
    fireEvent.click(openButton);
    const closeButton = screen.getByText('X');
    expect(closeButton).toBeVisible();
    expect(openButton).not.toBeVisible();

    // Click close button to hide sidebar
    fireEvent.click(closeButton);
    expect(openButton).toBeVisible();
    expect(closeButton).not.toBeVisible();
  });
});
