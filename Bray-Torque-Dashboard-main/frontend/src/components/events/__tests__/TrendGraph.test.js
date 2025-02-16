// __tests__/TrendGraph.test.jsx
import React from 'react';
import { render } from '@testing-library/react';
import TrendGraph from '../TrendGraph';
import '@testing-library/jest-dom';
import { AgCharts } from 'ag-charts-community';

jest.mock('ag-charts-community', () => ({
  AgCharts: {
    create: jest.fn(),
    destroy: jest.fn(),
  },
}));

describe('TrendGraph', () => {
  const mockData = [10, 20, 30, 40];
  const mockTitle = 'Test Chart';
  const mockDataKey = 'maxTorques';

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('renders TrendGraph component and initializes chart with correct options', () => {
    render(<TrendGraph title={mockTitle} dataKey={mockDataKey} data={mockData} />);

    expect(AgCharts.create).toHaveBeenCalledWith(
      expect.objectContaining({
        container: expect.any(HTMLElement),
        data: [
          { index: 1, value: 10 },
          { index: 2, value: 20 },
          { index: 3, value: 30 },
          { index: 4, value: 40 },
        ],
        title: { text: mockTitle },
        series: [
          expect.objectContaining({
            type: 'line',
            xKey: 'index',
            yKey: 'value',
          }),
        ],
        axes: [
          expect.objectContaining({
            type: 'category',
            position: 'bottom',
            title: { text: 'Events' },
          }),
          expect.objectContaining({
            type: 'number',
            position: 'left',
            title: { text: 'maxTorques (µV)' },
          }),
        ],
      })
    );
  });

  it('displays the correct tooltip content based on dataKey', () => {
    render(<TrendGraph dataKey="temperatures" data={[15, 25, 35]} />);

    // Check that tooltip configuration is set up correctly
    const { renderer } = AgCharts.create.mock.calls[0][0].series[0].tooltip;
    const tooltipContent = renderer({ datum: { value: 25 }, yKey: 'value' }).content;
    expect(tooltipContent).toBe('Temperature: 25 C');
  });
});
