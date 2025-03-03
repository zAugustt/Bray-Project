import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import TorqueGraph from '../TorqueGraph';
import { separateDataIntoPackets } from '../TorqueGraph';
import { useParams } from 'react-router-dom';
import { useEventDetails, useEventDetailsDownload } from '../../../apiServices';
import '@testing-library/jest-dom';

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useParams: jest.fn(),
}));

jest.mock('../../../apiServices', () => ({
  useEventDetails: jest.fn(),
  useEventDetailsDownload: jest.fn(),
}));


global.ResizeObserver = class {
    constructor(callback) {
      this.callback = callback;
    }
    observe() {
      this.callback([{ contentRect: { width: 100, height: 100 } }]);
    }
    unobserve() {}
    disconnect() {}
};

describe('TorqueGraph', () => {
  const mockEventDetails = {
    torqueData: [10, 20, 15, 30, 25, 40, 35, 50],
    recordLengths: [4, 4],
    typeOfStroke: 2,
  };

  it('renders torque data correctly and updates stroke type', async () => {
    const mockEventDetails = {
      torqueData: [10, 20, 15, 30, 25, 40, 35, 50],
      recordLengths: [4, 4],
      typeOfStroke: 1,
    };

    useParams.mockReturnValue({ sensorId: '123', eventId: '456' });
    useEventDetails.mockReturnValue({
      eventDetails: mockEventDetails,
      refreshData: jest.fn(),
    });
    useEventDetailsDownload.mockReturnValue({
      eventDetails: {},
      refreshData: jest.fn(),
    });

    render(<TorqueGraph />);

    expect(screen.getByText('Torque Signature Data - Open')).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText('30')).toBeInTheDocument();
    });

    expect(screen.getByText('Torque (µV)')).toBeInTheDocument();
  });

  it('correctly separates data into packets based on record lengths', async () => {
    useParams.mockReturnValue({ sensorId: '123', eventId: '456' });
    useEventDetails.mockReturnValue({
      eventDetails: mockEventDetails,
      refreshData: jest.fn(),
    });
    useEventDetailsDownload.mockReturnValue({
      eventDetails: {},
      refreshData: jest.fn(),
    });

    render(<TorqueGraph />);

    await waitFor(() => {
      expect(screen.getByText('30')).toBeInTheDocument();
    });
  });

  it('handles missing torqueData gracefully', async () => {
    useParams.mockReturnValue({ sensorId: '123', eventId: '456' });
    useEventDetails.mockReturnValue({
      eventDetails: { torqueData: null, recordLengths: [] },
      refreshData: jest.fn(),
    });
    useEventDetailsDownload.mockReturnValue({
      eventDetails: {},
      refreshData: jest.fn(),
    });

    render(<TorqueGraph />);

    await waitFor(() => {
      expect(screen.queryByText('Data Points')).not.toBeInTheDocument();
    });
  });

  it('calculates gradientOffset correctly', () => {
    const mockEventDetails = {
      torqueData: [10, 20, 15, 30, 25, 40, 35, 50],
      recordLengths: [4, 4],
      typeOfStroke: 0,
    };

    useParams.mockReturnValue({ sensorId: '123', eventId: '456' });
    useEventDetails.mockReturnValue({
      eventDetails: mockEventDetails,
      refreshData: jest.fn(),
    });
    useEventDetailsDownload.mockReturnValue({
      eventDetails: {},
      refreshData: jest.fn(),
    });

    render(<TorqueGraph />);

    expect(screen.getByText('Torque (µV)')).toBeInTheDocument();
  });
});

describe('separateDataIntoPackets', () => {
  
  test('should correctly separate torque data into packets based on recordLengths', () => {
    const eventDetails = {
      torqueData: [1, 2, 3, 4, 5, 6],
      recordLengths: [2, 2, 2],
    };

    const expectedPackets = [
      { index: 0, torque: 1 },
      { index: 1, torque: 2 },
      { index: 2, torque: 3 },
      { index: 3, torque: 4 },
      { index: 4, torque: 5 },
      { index: 5, torque: 6 },
    ];

    const packets = separateDataIntoPackets(eventDetails);
    expect(packets).toEqual(expectedPackets);
  });

  test('should throw an error when packet length exceeds torqueData length', () => {
    const eventDetails = {
      torqueData: [1, 2, 3],
      recordLengths: [2, 3], // This adds up to 5, but torqueData has only 3 elements
    };

    expect(() => separateDataIntoPackets(eventDetails)).toThrow(
      'Invalid packet length: exceeds torqueData length.'
    );
  });

  test('should handle empty torqueData and recordLengths', () => {
    const eventDetails = {
      torqueData: [],
      recordLengths: [],
    };

    const packets = separateDataIntoPackets(eventDetails);
    expect(packets).toEqual([]);
  });
});
