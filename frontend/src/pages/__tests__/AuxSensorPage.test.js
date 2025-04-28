import React from "react";
import { render, screen } from "@testing-library/react";
import AuxDetailsContainer from "../../components/auxSensor/AuxDetailsContainer";
import '@testing-library/jest-dom';

jest.mock('../../components/Header', () => () => <div>Mock Header</div>);
jest.mock('../../components/auxSensor/AuxDetailsContainer', () => () => <div>Mock AuxDetailsContainer</div>);

describe('AuxSensorPage', () => {
    it('renders Header and AuxDetailContainer components', () => {
        render(<AuxDetailsContainer />);

        
        expect(screen.getByText('Mock AuxDetailsContainer')).toBeInTheDocument();
    })
})