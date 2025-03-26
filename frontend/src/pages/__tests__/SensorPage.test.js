import React from 'react';
import { render, screen, fireEvent, waitFor  } from '@testing-library/react';
import SensorPage from '../SensorPage';
import { useSensorData } from '../../apiServices';
import { MemoryRouter } from 'react-router-dom';

// Mock the useSensorData hook to return a single row of data
jest.mock('../../apiServices', () => ({
    useSensorData: jest.fn(),
}));

describe('SensorPage', () => {
    beforeEach(() => {
        // Mock data to simulate one row of data
        useSensorData.mockReturnValue({
            sensorData: [
                { id: '1', sensorName: 'emission', serialNumber: '555AB29', numEvents: 2 }
            ],
            refreshData: jest.fn(),
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
        expect(screen.getByText('555AB29')).toBeInTheDocument();

        const row = screen.getByText('555AB29'); // Select the row by its content
        fireEvent.click(row);

        await waitFor(() =>
            expect(screen.getByText('2')).toBeInTheDocument()
        );
    });
});
