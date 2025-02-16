import React from 'react';
import { render, screen } from '@testing-library/react';
import EventPage from '../EventPage';
import '@testing-library/jest-dom';

jest.mock('../../components/Header', () => () => <div>Mock Header</div>);
jest.mock('../../components/events/EventsContainer', () => () => <div>Mock EventsContainer</div>);

describe('EventPage', () => {
  it('renders Header and EventsContainer components', () => {
    render(<EventPage />);

    expect(screen.getByText('Mock Header')).toBeInTheDocument();
    expect(screen.getByText('Mock EventsContainer')).toBeInTheDocument();
  });
});
