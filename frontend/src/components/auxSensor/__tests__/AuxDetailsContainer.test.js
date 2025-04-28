import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter, Route, Routes } from 'react-router-dom';
import AuxDetailsContainer from '../AuxDetailsContainer';
import { useAuxData } from '../../../apiServices';
import '@testing-library/jest-dom/extend-expect';

jest.mock('../../../apiServices', () => ({
    useAuxData: jest.fn(),
}));

jest.mock('../AuxGraph', () => () => <div>Mocked AuxGraph</div>);

describe('AuxDetailsContainer', () => {
    const mockAuxData = [{
        id: 2,
        timestamp: '2025-04-11 17:58:27.130108',
        percentage: 168
    }];

    beforeEach(() => {
        useAuxData.mockReturnValue({ auxData: mockAuxData });
    });
    
    test('renders AuxDetailsContainer with correct data', () => {
        render(
            <MemoryRouter initialEntries={['/aux_sensors/2']}>
                <Routes>
                    <Route path="/aux_sensors/:auxSensorID" element={<AuxDetailsContainer />} />
                </Routes>
            </MemoryRouter>
        );

        expect(screen.getByText(`Aux Sensor ${mockAuxData[0].id} - ${mockAuxData[0].timestamp}`)).toBeInTheDocument();
    })
})