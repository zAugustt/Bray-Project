import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import SensorTable from '../SensorTable';
import { useAuxSensorData, useSensorData } from '../../../apiServices';
import { MemoryRouter } from 'react-router-dom';

// Mock the useSensorData hook to return a single row of data
jest.mock('../../../apiServices', () => ({
    useSensorData: jest.fn(),
    useAuxSensorData: jest.fn(),
}));

describe('SensorTable', () => {
    beforeEach(() => {
        // Mock data to simulate one row of data
        useSensorData.mockReturnValue({
            sensorData: [
                { id: '1', devEUI: '00-14-22-01-23-45', numEvents: 2 }
            ],
            refreshData: jest.fn(),
        });

        useAuxSensorData.mockReturnValue({
            auxSensorData: [
                    { id: '4', devEUI: '39-33-33-32-56-32-78-14', numEvents: -1}
            ],
            refreshAuxData: jest.fn(),
        });
    });

    it('renders one row of sensor data', () => {
        render(
            <MemoryRouter>
                <SensorTable />
            </MemoryRouter>
        );
        
        // Check if the mock data row is displayed in the grid
        expect(screen.getByText('1')).toBeInTheDocument();
        expect(screen.getByText('00-14-22-01-23-45')).toBeInTheDocument();

        expect(screen.getByText('4')).toBeInTheDocument();
        expect(screen.getByText('39-33-33-32-56-32-78-14')).toBeInTheDocument();
    });

    it('refreshes data on RefreshButton click', () => {
        const { refreshData } = useSensorData();
        render(
            <MemoryRouter>
                <SensorTable />
            </MemoryRouter>
        );

        // Find the RefreshButton by its role or label
        const refreshButton = screen.getByRole('button', { name: /refresh/i });
        fireEvent.click(refreshButton);

        // Verify that refreshData was called
        expect(refreshData).toHaveBeenCalled();
    });
});
