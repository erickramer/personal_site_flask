# TODO Improvements

## Application Structure

- [ ] **Resolve Circular Import Issues**  
  Fix the circular dependency problems between app.py and sentiment modules. Implement a proper application factory pattern where models are defined separately, and ensure blueprints are correctly registered without import conflicts.

- [ ] **Complete Blueprint Implementation**  
  Properly implement the sentiment blueprint that is currently disabled. Restructure the code to avoid circular imports while maintaining the modular architecture intended with the blueprint design.

- [ ] **Implement Application Configuration**  
  Move hardcoded configuration from app.py to a config.py module with different environment configurations. Separate development, testing, and production settings to make the application more maintainable and deployable.

## Code Quality

- [ ] **Implement Error Handling**  
  Replace bare except blocks in sentiment/ml.py with specific exception handling. Add proper error responses with appropriate HTTP status codes for API endpoints to improve debugging and user experience.

- [ ] **Add Testing Infrastructure**  
  Create a comprehensive test suite with pytest fixtures for both unit and integration tests. Focus particularly on the sentiment analysis functionality to ensure accuracy and reliability of predictions.

- [x] **Modernize Dependencies**  
  Update requirements.txt to include specific version numbers and add missing dependencies like tensorflow. Consider using Poetry or Pipenv for better dependency management and reproducible environments.

## Security

- [ ] **Secure Static Asset References**  
  Fix relative paths in templates/base.html that may break in subdirectories. Use Flask's url_for() function for all static asset references to ensure they work correctly across the application.

- [ ] **Implement API Security**  
  Add CSRF protection and input validation on API endpoints in sentiment/views.py. Implement rate limiting and consider adding authentication for any sensitive operations to protect against abuse.

## Frontend

- [ ] **Organize Frontend Assets**  
  Implement a proper frontend build process with minification and bundling. Consider consolidating the multiple JS libraries or fully committing to Elm architecture throughout more of the application.

## Performance

- [ ] **Optimize Model Loading**  
  Move the SentimentModel initialization out of the request path in views.py to avoid initializing for each request. Implement a caching strategy for model predictions to reduce computation time for repeated inputs.