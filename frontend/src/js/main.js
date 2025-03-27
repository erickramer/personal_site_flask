// Import global CSS
import '../css/normalize.css';
import '../css/skeleton.css';

// Import dependencies
import $ from 'jquery';

// Export for global use
window.$ = window.jQuery = $;

// Common functionality used across all pages
document.addEventListener('DOMContentLoaded', function() {
  console.log('Main script loaded');
  
  // Add custom CSS to enable pointer events on SVG links
  const style = document.createElement('style');
  style.textContent = 'svg a, svg text, svg tspan { pointer-events: auto !important; }';
  document.head.appendChild(style);
});