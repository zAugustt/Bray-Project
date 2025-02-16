import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { MemoryRouter, useNavigate } from 'react-router-dom';
import ViewEventsButton from '../ViewEventsButton';

const mockNavigate = jest.fn(); // Create a mock function for navigation

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

describe('ViewEventsButton', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('navigates to the correct path with row data on button click', () => {
    const mockProps = {
      data: { id: '123', otherField: 'Test Data' },
    };

    render(
      <MemoryRouter>
        <ViewEventsButton {...mockProps} />
      </MemoryRouter>
    );

    const button = screen.getByText('View Events');
    fireEvent.click(button);

    expect(mockNavigate).toHaveBeenCalledWith(`/events/123`, {
      state: { rowData: mockProps.data },
    });
  });
});
