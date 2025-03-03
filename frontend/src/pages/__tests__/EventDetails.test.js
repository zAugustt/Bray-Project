import React from 'react';
import { render, screen } from '@testing-library/react';
import EventDetailsPage from '../EventDetailsPage';
import '@testing-library/jest-dom';

jest.mock('../../components/Header', () => () => <div>Mock Header</div>);
jest.mock('../../components/event-details/DetailsContainer', () => () => <div>Mock DetailsContainer</div>);

describe('EventDetailsPage', () => {
  it('renders Header and DetailsContainer components', () => {
    render(<EventDetailsPage />);

    // Check if the Header and DetailsContainer components are rendered
    expect(screen.getByText('Mock Header')).toBeInTheDocument();
    expect(screen.getByText('Mock DetailsContainer')).toBeInTheDocument();
  });
});
