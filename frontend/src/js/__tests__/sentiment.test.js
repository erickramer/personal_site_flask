/**
 * Tests for sentiment.js
 */

// Mock imports
jest.mock('d3', () => ({
  select: jest.fn().mockReturnThis(),
  empty: jest.fn().mockReturnValue(false),
}));
jest.mock('../../../css/sentiment.css', () => ({}));

// Set up fetch mock
beforeEach(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({
        emoji: { '😊': 0.9, '😢': 0.1 },
        sentiment: 0.8
      })
    })
  );
});

// Set up test DOM
beforeEach(() => {
  document.body.innerHTML = `
    <div class="container">
      <textarea id="target">Test text</textarea>
      <button>Test Button</button>
      <div id="visualization">
        <svg></svg>
      </div>
    </div>
  `;
});

// Import module after setting up mocks
import '../sentiment.js';

describe('Sentiment Module', () => {
  test('DOM elements are properly selected', () => {
    const textarea = document.getElementById('target');
    expect(textarea).toBeTruthy();
    expect(textarea.value).toBe('Test text');
  });

  test('Button click submits text for analysis', () => {
    const button = document.querySelector('button');
    const textarea = document.getElementById('target');
    
    // Click the button
    button.click();
    
    // Check that fetch was called with the right parameters
    expect(global.fetch).toHaveBeenCalledWith('/sentiment/api/score', {
      method: 'POST',
      body: expect.any(FormData),
    });
  });

  test('textarea input triggers analysis after debounce', (done) => {
    const textarea = document.getElementById('target');
    
    // Simulate input
    textarea.value = 'New text value';
    const event = new Event('input');
    textarea.dispatchEvent(event);
    
    // Wait for debounce
    setTimeout(() => {
      expect(global.fetch).toHaveBeenCalledWith('/sentiment/api/score', {
        method: 'POST',
        body: expect.any(FormData),
      });
      done();
    }, 600); // Slightly longer than debounce timeout
  });
  
  test('Empty text does not trigger API call', () => {
    const textarea = document.getElementById('target');
    textarea.value = '';
    
    const event = new Event('input');
    textarea.dispatchEvent(event);
    
    // Check fetch wasn't called
    expect(global.fetch).not.toHaveBeenCalled();
  });
});