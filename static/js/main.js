document.addEventListener('DOMContentLoaded', function () {
  // Provide a simple hook for page-specific scripts to detect initialisation.
  window.dispatchEvent(new CustomEvent('app:ready'));
});
