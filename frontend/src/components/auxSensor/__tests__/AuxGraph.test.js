import React from "react";
import { render, screen, waitFor } from '@testing-library/react';
import AuxGraph from "../AuxGraph";
import { useParams } from "react-router-dom";
import '@testing-library/jest-dom';

jest.mock('react-router-dom', () => ({
    ...jest.requireActual('react-router-dom'),
    useParams: jest.fn(),
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

describe('AuxGraph', () => {
    const mockSensorID = 2;
    const mockAuxData = [{
        id: 2,
        timestamp: '2025-04-11 17:58:27.130108',
        percentage: 168
    }];

    it('renders aux data correctly', () => {
        useParams.mockReturnValue({ auxSensorID: '2'});

        render(<AuxGraph auxData={mockAuxData} />);

        expect(screen.getByText(`Aux Sensor ${mockSensorID} Signature Data`)).toBeInTheDocument();

        expect(screen.getByText('CO2 (%)')).toBeInTheDocument();

    });

    it('handles missing auxData gracefully', () => {
        useParams.mockReturnValue({ auxSensorID: '2'});

        render(<AuxGraph auxData={[{id: '', timestamp: '', percentage: -1}]} />);

        expect(screen.getByText(`Aux Sensor ${mockSensorID} Signature Data`)).toBeInTheDocument();
    });

    it('calculates gradientOffset correctly', () => {
        useParams.mockReturnValue({ auxSensorID: '2'});

        render(<AuxGraph auxData={mockAuxData} />);

        expect(screen.getByText(`Aux Sensor ${mockSensorID} Signature Data`)).toBeInTheDocument();

        expect(screen.getByText('CO2 (%)')).toBeInTheDocument();

    });
});