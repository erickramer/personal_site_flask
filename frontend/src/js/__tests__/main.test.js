/**
 * Tests for main.js
 */

// We need to mock the CSS imports before importing the main file
jest.mock('../../../css/normalize.css', () => ({}));
jest.mock('../../../css/skeleton.css', () => ({}));

// Import the module to test
import '../main.js';

describe('Main JS', () => {
  // Set up the DOM for testing
  document.body.innerHTML = `
    <div id="content">
      <h1>Test Content</h1>
    </div>
  `;
  
  // Test that jQuery is properly initialized
  test('jQuery is properly initialized', () => {
    expect(window.$).toBeDefined();
    expect(window.jQuery).toBeDefined();
    expect($('#content').length).toBe(1);
  });
  
  // Test that the main script loaded
  test('Main script loads and runs', () => {
    // Create a spy on console.log
    const consoleSpy = jest.spyOn(console, 'log');
    
    // Trigger the DOMContentLoaded event
    const event = new Event('DOMContentLoaded');
    document.dispatchEvent(event);
    
    // Check if console.log was called with the expected message
    expect(consoleSpy).toHaveBeenCalledWith('Main script loaded');
    
    // Restore the original console.log
    consoleSpy.mockRestore();
  });
});