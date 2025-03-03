import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import DownloadButton from '../DownloadButton';
import { useEventDetailsDownload } from '../../../apiServices';
import { useParams } from 'react-router-dom';

jest.mock('../../../apiServices', () => ({
  useEventDetailsDownload: jest.fn(),
}));

jest.mock('react-router-dom', () => ({
  useParams: jest.fn(),
}));


global.URL.createObjectURL = jest.fn(() => 'mocked-url');
global.URL.revokeObjectURL = jest.fn();

describe('DownloadButton', () => {
  beforeEach(() => {
    useParams.mockReturnValue({ sensorId: '1', eventId: '2' });

    useEventDetailsDownload.mockReturnValue({
      eventDetails: new Blob(['mocked csv content'], { type: 'text/csv' }),
    });
  });

  test('renders the download button', () => {
    render(<DownloadButton />);
    expect(screen.getByText('Download CSV')).toBeInTheDocument();
  });

  test('triggers CSV download when the button is clicked', () => {
    const createObjectURLSpy = jest.spyOn(window.URL, 'createObjectURL');
    const revokeObjectURLSpy = jest.spyOn(window.URL, 'revokeObjectURL');
    const appendChildSpy = jest.spyOn(document.body, 'appendChild');
    const removeChildSpy = jest.spyOn(document.body, 'removeChild');

    render(<DownloadButton />);

    const downloadButton = screen.getByText('Download CSV');
    fireEvent.click(downloadButton);

    expect(createObjectURLSpy).toHaveBeenCalledWith(expect.any(Blob));

    expect(appendChildSpy).toHaveBeenCalled();
    expect(removeChildSpy).toHaveBeenCalled();

    expect(revokeObjectURLSpy).toHaveBeenCalled();

    createObjectURLSpy.mockRestore();
    revokeObjectURLSpy.mockRestore();
    appendChildSpy.mockRestore();
    removeChildSpy.mockRestore();
  });

  test('logs an error if eventDetails is missing', () => {
    console.error = jest.fn(); 

    useEventDetailsDownload.mockReturnValue({
      eventDetails: null,
    });

    render(<DownloadButton />);

    const downloadButton = screen.getByText('Download CSV');
    fireEvent.click(downloadButton);

    expect(console.error).toHaveBeenCalledWith('No event details available for download.');
  });
});
