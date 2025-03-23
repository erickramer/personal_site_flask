// Sentiment analysis page scripts
import * as d3 from 'd3';

// Import specific styles
import '../css/sentiment.css';

document.addEventListener('DOMContentLoaded', function() {
  console.log('Sentiment analysis page loaded');
  
  // Setup the visualization
  setupVisualization();
  
  // Attach event listeners to tweet input
  setupEventListeners();
});

function setupVisualization() {
  // D3 visualization code goes here
  const svg = d3.select('#visualization svg');
  
  if (!svg.empty()) {
    // Setup D3 visualization (simplified version of viz.js)
    // This would be the code from the original viz.js file
  }
}

function setupEventListeners() {
  const textarea = document.getElementById('target');
  
  if (textarea) {
    textarea.addEventListener('input', debounce(function() {
      submitTextForAnalysis(textarea.value);
    }, 500));
    
    // Add demo button event listeners
    document.querySelectorAll('button').forEach(button => {
      button.addEventListener('click', function() {
        textarea.value = this.textContent;
        submitTextForAnalysis(textarea.value);
      });
    });
  }
}

function submitTextForAnalysis(text) {
  if (!text.trim()) return;
  
  const formData = new FormData();
  formData.append('text', text);
  
  fetch('/sentiment/api/score', {
    method: 'POST',
    body: formData,
  })
    .then(response => response.json())
    .then(data => {
      updateVisualization(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

function updateVisualization(data) {
  // Update the D3 visualization with the returned data
  console.log('Sentiment data received:', data);
  
  // This would call functions from the original viz.js to update the visualization
}

// Utility function to debounce API calls
function debounce(func, wait) {
  let timeout;
  return function() {
    const context = this;
    const args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      func.apply(context, args);
    }, wait);
  };
}