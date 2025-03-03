import reportWebVitals from '../reportWebVitals';

jest.mock('web-vitals', () => ({
  getCLS: jest.fn(),
  getFID: jest.fn(),
  getFCP: jest.fn(),
  getLCP: jest.fn(),
  getTTFB: jest.fn(),
}));

describe('reportWebVitals', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should not call any web-vitals functions if onPerfEntry is not provided', async () => {
    reportWebVitals(null);

    const webVitals = await import('web-vitals');
    expect(webVitals.getCLS).not.toHaveBeenCalled();
    expect(webVitals.getFID).not.toHaveBeenCalled();
    expect(webVitals.getFCP).not.toHaveBeenCalled();
    expect(webVitals.getLCP).not.toHaveBeenCalled();
    expect(webVitals.getTTFB).not.toHaveBeenCalled();
  });

  it('should not call any web-vitals functions if onPerfEntry is not a function', async () => {
    reportWebVitals({}); // Passing an object instead of a function

    const webVitals = await import('web-vitals');
    expect(webVitals.getCLS).not.toHaveBeenCalled();
    expect(webVitals.getFID).not.toHaveBeenCalled();
    expect(webVitals.getFCP).not.toHaveBeenCalled();
    expect(webVitals.getLCP).not.toHaveBeenCalled();
    expect(webVitals.getTTFB).not.toHaveBeenCalled();
  });
});
