import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import DetailsContainer from '../DetailsContainer';
import { useSensorData, useSensorEvents } from '../../../apiServices';
import '@testing-library/jest-dom/extend-expect';

jest.mock('../../../apiServices', () => ({
  useSensorEvents: jest.fn(),
  useSensorData: jest.fn(),
}));

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: jest.fn(),
}));

jest.mock('../TorqueGraph', () => () => <div>Mocked TorqueGraph</div>);
jest.mock('../PacketInfo', () => () => <div>Mocked PacketInfo</div>);

describe('DetailsContainer', () => {
  const mockNavigate = jest.fn();
  const mockSensorEvents = {
    event_datas: [
      { timestamp: '2023-11-11 10:00:00' },
      { timestamp: '2023-11-11 11:00:00' },
    ],
  };

  const mockSensorData = [
    { numEvents: 2 },
  ];

  beforeEach(() => {
    require('react-router-dom').useNavigate.mockReturnValue(mockNavigate);
    useSensorEvents.mockReturnValue({ sensorEvents: mockSensorEvents });
    useSensorData.mockReturnValue({ sensorData: mockSensorData });
  });

  test('renders DetailsContainer with correct data', () => {
    render(
      <MemoryRouter initialEntries={['/events/1/event-details/1']}>
        <Routes>
          <Route path="/events/:sensorId/event-details/:eventId" element={<DetailsContainer />} />
        </Routes>
      </MemoryRouter>
    );

    expect(screen.getByText('Sensor 1, Event 1 - 2023-11-11 10:00:00')).toBeInTheDocument();
  });

  test('navigates to the previous event when Prev button is clicked', () => {
    render(
      <MemoryRouter initialEntries={['/events/2/event-details/2']}>
        <Routes>
          <Route path="/events/:sensorId/event-details/:eventId" element={<DetailsContainer />} />
        </Routes>
      </MemoryRouter>
    );

    const prevButton = screen.getByText('Prev');
    fireEvent.click(prevButton);

    expect(mockNavigate).toHaveBeenCalledWith('/events/2/event-details/1');
  });

  test('navigates to the next event when Next button is clicked', () => {
    render(
      <MemoryRouter initialEntries={['/events/1/event-details/1']}>
        <Routes>
          <Route path="/events/:sensorId/event-details/:eventId" element={<DetailsContainer />} />
        </Routes>
      </MemoryRouter>
    );

    const nextButton = screen.getByText('Next');
    fireEvent.click(nextButton);

    expect(mockNavigate).toHaveBeenCalledWith('/events/1/event-details/2');
  });

  test('does not navigate beyond first event', () => {
    render(
      <MemoryRouter initialEntries={['/events/1/event-details/1']}>
        <Routes>
          <Route path="/events/:sensorId/event-details/:eventId" element={<DetailsContainer />} />
        </Routes>
      </MemoryRouter>
    );

    const prevButton = screen.getByText('Prev');
    fireEvent.click(prevButton);

    expect(mockNavigate).not.toHaveBeenCalled();
  });

  test('does not navigate beyond last event', () => {
    render(
      <MemoryRouter initialEntries={['/events/1/event-details/2']}>
        <Routes>
          <Route path="/events/:sensorId/event-details/:eventId" element={<DetailsContainer />} />
        </Routes>
      </MemoryRouter>
    );

    const nextButton = screen.getByText('Next');
    fireEvent.click(nextButton);

    expect(mockNavigate).not.toHaveBeenCalled();
  });
});
