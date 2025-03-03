import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import EventTable from '../EventTable';
import '@testing-library/jest-dom';
import { useParams } from 'react-router-dom';
import { useSensorEvents } from '../../../apiServices';

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useParams: jest.fn(),
}));

jest.mock('../../../apiServices', () => ({
  useSensorEvents: jest.fn(),
}));

describe('EventTable', () => {
  beforeEach(() => {
    jest.clearAllMocks();

    useParams.mockReturnValue({ sensorId: '123' });

    useSensorEvents.mockReturnValue({
      sensorEvents: {
        event_datas: [
          { id: '1', timestamp: '2024-11-01T12:00:00Z' },
          { id: '2', timestamp: '2024-11-02T13:00:00Z' },
        ],
      },
      refreshData: jest.fn(),
    });
  });

  it('renders EventTable component with data and buttons', () => {
    render(
      <MemoryRouter>
        <EventTable />
      </MemoryRouter>
    );

    // Check if the BackButton and RefreshButton are present
    expect(screen.getByRole('button', { name: /back/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /refresh/i })).toBeInTheDocument();

    // Check if the title is correct
    expect(screen.getByText('Historical Data for Sensor 123')).toBeInTheDocument();
  });

  it('updates rowData when sensorEvents changes', () => {
    render(
      <MemoryRouter>
        <EventTable />
      </MemoryRouter>
    );

    // Check that the grid renders data from mock sensorEvents
    const rows = screen.getAllByRole('row');
    expect(rows.length).toBeGreaterThan(1); // Ensure data rows are rendered

    // Check specific cells in the first row for expected data
    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('2024-11-01T12:00:00Z')).toBeInTheDocument();
  });
});
