import React from 'react';
import { render, screen, fireEvent, waitFor  } from '@testing-library/react';
import SensorPage from '../SensorPage';
import { useAuxSensorData, useSensorData } from '../../apiServices';
import { MemoryRouter } from 'react-router-dom';

// Mock the useSensorData hook to return a single row of data
jest.mock('../../apiServices', () => ({
    useSensorData: jest.fn(),
    useAuxSensorData: jest.fn(),
}));

describe('SensorPage', () => {
    beforeEach(() => {
        // Mock data to simulate one row of data
        useSensorData.mockReturnValue({
            sensorData: [
                { id: '1', devEUI: '00-00-00-01-03-45', numEvents: 2 }
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

    it('click row should fill container', async () => {
        render(
            <MemoryRouter>
                <SensorPage />
            </MemoryRouter>
        );
        
        // Check if the mock data row is displayed in the grid
        expect(screen.getByText('1')).toBeInTheDocument();
        expect(screen.getByText('00-00-00-01-03-45')).toBeInTheDocument();

        expect(screen.getByText('4')).toBeInTheDocument();
        expect(screen.getByText('39-33-33-32-56-32-78-14')).toBeInTheDocument();

        const row = screen.getByText('00-00-00-01-03-45'); // Select the row by its content
        fireEvent.click(row);

        await waitFor(() =>
            expect(screen.getByText('2')).toBeInTheDocument()
        );

        const auxRow = screen.getByText('39-33-33-32-56-32-78-14');
        fireEvent.click(auxRow);

        await waitFor(() =>
            expect(screen.getByText('Aux Sensor')).toBeInTheDocument()
        );
    });
});
