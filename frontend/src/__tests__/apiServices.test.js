import { useSensorData, useSensorEvents, useEventDetails, useEventDetailsDownload } from '../apiServices';
import { renderHook, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';

global.fetch = jest.fn();

describe('Custom Hook Tests', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('useSensorData', () => {
    it('fetches sensor data successfully', async () => {
      const mockData = [{ id: 1, name: 'Sensor 1' }];
      fetch.mockResolvedValue({
        ok: true,
        json: async () => mockData,
      });
  
      const { result, waitForNextUpdate } = renderHook(() => useSensorData());
  
      await waitFor(() => {
        expect(result.current.sensorData).toEqual(mockData);
      });

      expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api_v1/sensors');
    });

    it('handles fetch error', async () => {
      fetch.mockRejectedValueOnce(new Error('Network response was not ok'));

      const { result, waitForNextUpdate } = renderHook(() => useSensorData());

      await waitFor(() => {
        expect(result.current.sensorData).toEqual([]);
      });      
      
      expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api_v1/sensors');
    });
  });

  describe('useSensorEvents', () => {
    it('fetches sensor events successfully', async () => {
      const mockSensorId = '123';
      const mockEvents = [{ id: 1, eventName: 'Event 1' }];
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockEvents,
      });

      const { result, waitForNextUpdate } = renderHook(() => useSensorEvents(mockSensorId));

      await waitFor(() => {
        expect(result.current.sensorEvents).toEqual(mockEvents);
      });

      expect(fetch).toHaveBeenCalledWith(`http://localhost:5000/api_v1/sensors/${mockSensorId}/events`);
    });

    it('handles fetch error in useSensorEvents', async () => {
      const mockSensorId = '123';
      fetch.mockRejectedValueOnce(new Error('Network response was not ok'));

      const { result, waitForNextUpdate } = renderHook(() => useSensorEvents(mockSensorId));

      await waitFor(() => {
        expect(result.current.sensorEvents).toEqual([]);
      });

      expect(fetch).toHaveBeenCalledWith(`http://localhost:5000/api_v1/sensors/${mockSensorId}/events`);
    });
  });

  describe('useEventDetails', () => {
    it('fetches event details successfully', async () => {
      const mockSensorId = '123';
      const mockEventId = '456';
      const mockEventDetails = { id: 456, name: 'Event Details' };
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockEventDetails,
      });

      const { result, waitForNextUpdate } = renderHook(() => useEventDetails(mockSensorId, mockEventId, { hidden: false }));
      
      expect(fetch).toHaveBeenCalledWith(`http://localhost:5000/api_v1/sensors/${mockSensorId}/events/${mockEventId}`);
    });

    it('handles fetch error in useEventDetails', async () => {
      const mockSensorId = '123';
      const mockEventId = '456';
      fetch.mockRejectedValueOnce(new Error('Network response was not ok'));

      const { result, waitForNextUpdate } = renderHook(() => useEventDetails(mockSensorId, mockEventId, { hidden: false }));

      await waitFor(() => {
        expect(result.current.eventDetails).toEqual([]);
      });

      expect(fetch).toHaveBeenCalledWith(`http://localhost:5000/api_v1/sensors/${mockSensorId}/events/${mockEventId}`);
    });
  });

  describe('useEventDetailsDownload', () => {
    it('fetches and sets event details as Blob (with hidden parameter)', async () => {
      const mockBlob = new Blob(['mocked csv content'], { type: 'text/csv' });
      fetch.mockResolvedValueOnce({
        ok: true,
        blob: () => Promise.resolve(mockBlob),
      });

      const { result, waitForNextUpdate } = renderHook(() => useEventDetailsDownload('1', '1', { hidden: true }));

      await waitFor(() => {
        expect(result.current.eventDetails).toEqual(mockBlob);
      });

      expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api_v1/sensors/1/events/1/download/hidden');
    });

    it('fetches and sets event details as Blob (without hidden parameter)', async () => {
      const mockBlob = new Blob(['mocked csv content'], { type: 'text/csv' });
      fetch.mockResolvedValueOnce({
        ok: true,
        blob: () => Promise.resolve(mockBlob),
      });

      const { result, waitForNextUpdate } = renderHook(() => useEventDetailsDownload('1', '1', { hidden: false }));

      await waitFor(() => {
        expect(result.current.eventDetails).toEqual(mockBlob);
      });

      expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api_v1/sensors/1/events/1/download');
    });

    it('handles network error in useEventDetailsDownload', async () => {
      fetch.mockRejectedValueOnce(new Error('Network error'));

      const { result, waitForNextUpdate } = renderHook(() => useEventDetailsDownload('1', '1', { hidden: false }));

      expect(result.current.eventDetails).toBeNull();
      expect(fetch).toHaveBeenCalledWith('http://localhost:5000/api_v1/sensors/1/events/1/download');
    });
  });
});
