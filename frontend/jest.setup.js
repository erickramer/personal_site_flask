// Import jest-dom additions
import '@testing-library/jest-dom';

// Mock fetch
global.fetch = jest.fn();

// Mock DOM functions that might not be available in jsdom
window.matchMedia = window.matchMedia || function() {
  return {
    matches: false,
    addListener: function() {},
    removeListener: function() {}
  };
};

// Set up jQuery mock
global.$ = global.jQuery = require('jquery');

// Mock D3 if needed for certain tests
jest.mock('d3', () => {
  const originalD3 = jest.requireActual('d3');
  return {
    ...originalD3,
    // You can override specific D3 methods here if needed
  };
});