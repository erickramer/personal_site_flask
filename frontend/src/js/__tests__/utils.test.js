/**
 * Tests for utility functions
 */

import { 
  debounce, 
  formatPercentage, 
  truncateText, 
  safeJsonParse 
} from '../utils';

// Tests for debounce function
describe('debounce', () => {
  jest.useFakeTimers();

  test('debounce executes the function after the specified delay', () => {
    const mockFn = jest.fn();
    const debouncedFn = debounce(mockFn, 300);

    // Call the debounced function
    debouncedFn();
    
    // Function should not be called immediately
    expect(mockFn).not.toHaveBeenCalled();

    // Fast-forward time
    jest.advanceTimersByTime(300);
    
    // Now the function should have been called
    expect(mockFn).toHaveBeenCalled();
    expect(mockFn).toHaveBeenCalledTimes(1);
  });

  test('multiple calls to debounced function only execute once', () => {
    const mockFn = jest.fn();
    const debouncedFn = debounce(mockFn, 300);

    // Call debounced function multiple times
    debouncedFn();
    debouncedFn();
    debouncedFn();
    
    // Function should not be called yet
    expect(mockFn).not.toHaveBeenCalled();

    // Fast-forward time
    jest.advanceTimersByTime(300);
    
    // Function should have been called only once
    expect(mockFn).toHaveBeenCalledTimes(1);
  });
});

// Tests for formatPercentage function
describe('formatPercentage', () => {
  test('formats decimal numbers as percentages', () => {
    expect(formatPercentage(0.5)).toBe('50.0%');
    expect(formatPercentage(0.125)).toBe('12.5%');
    expect(formatPercentage(1)).toBe('100.0%');
    expect(formatPercentage(0)).toBe('0.0%');
  });
});

// Tests for truncateText function
describe('truncateText', () => {
  test('returns original text if shorter than max length', () => {
    const text = 'Short text';
    expect(truncateText(text, 20)).toBe(text);
  });

  test('truncates text if longer than max length', () => {
    const text = 'This is a long text that should be truncated';
    expect(truncateText(text, 10)).toBe('This is a ...');
  });

  test('handles null or undefined input', () => {
    expect(truncateText(null, 10)).toBe(null);
    expect(truncateText(undefined, 10)).toBe(undefined);
  });

  test('uses default max length if not specified', () => {
    const longText = 'a'.repeat(150);
    const result = truncateText(longText);
    expect(result.length).toBe(103); // 100 chars + 3 for '...'
  });
});

// Tests for safeJsonParse function
describe('safeJsonParse', () => {
  // Silence console.error for these tests
  let originalConsoleError;
  
  beforeEach(() => {
    // Save original console.error
    originalConsoleError = console.error;
    // Replace with no-op function
    console.error = jest.fn();
  });
  
  afterEach(() => {
    // Restore original console.error
    console.error = originalConsoleError;
  });
  
  test('correctly parses valid JSON', () => {
    const jsonString = '{"name":"test","value":123}';
    expect(safeJsonParse(jsonString)).toEqual({name: 'test', value: 123});
  });

  test('returns fallback on invalid JSON', () => {
    const invalidJson = '{invalid: json}';
    expect(safeJsonParse(invalidJson)).toEqual({});
  });

  test('accepts custom fallback value', () => {
    const invalidJson = '{invalid: json}';
    const fallback = {error: true};
    expect(safeJsonParse(invalidJson, fallback)).toBe(fallback);
  });

  test('handles array JSON', () => {
    const jsonArray = '[1,2,3]';
    expect(safeJsonParse(jsonArray)).toEqual([1, 2, 3]);
  });
  
  test('logs error when JSON is invalid', () => {
    const invalidJson = '{invalid: json}';
    safeJsonParse(invalidJson);
    expect(console.error).toHaveBeenCalled();
  });
});