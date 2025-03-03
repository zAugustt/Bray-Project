import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import PacketInfo from '../PacketInfo';
import { useEventDetails } from '../../../apiServices';
import { useParams } from 'react-router-dom';
import '@testing-library/jest-dom';

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useParams: jest.fn(),
}));

jest.mock('../../../apiServices', () => ({
  useEventDetails: jest.fn(),
}));

describe('PacketInfo', () => {
  it('renders event details correctly', async () => {
    useParams.mockReturnValue({ sensorId: '123', eventId: '456' });

    useEventDetails.mockReturnValue({
      eventDetails: {
        eventName: 'Test Event',
        timestamp: '2024-11-05',
        batteryVoltage: '3.7',
        torqueData: 'deleted'
      },
      refreshData: jest.fn(),
    });

    render(<PacketInfo />);

    await waitFor(() => {
      expect(screen.getByText('Test Event')).toBeInTheDocument();
      expect(screen.getByText('2024-11-05')).toBeInTheDocument();
      expect(screen.getByText('3.7')).toBeInTheDocument();
      expect(screen.queryByText('deleted')).not.toBeInTheDocument();
    });
  });

  it('handles empty event details', async () => {
    useParams.mockReturnValue({ sensorId: '123', eventId: '456' });
    useEventDetails.mockReturnValue({
      eventDetails: {},
      refreshData: jest.fn(),
    });

    render(<PacketInfo />);

    await waitFor(() => {
      expect(screen.getByText('LoRa Event Data')).toBeInTheDocument();
      expect(screen.queryByText(/:/)).toBeNull();
    });
  });
});
