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
});