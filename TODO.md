# TODO Improvements

## Application Structure

- [x] **Resolve Circular Import Issues**  
  Fix the circular dependency problems between app.py and sentiment modules. Implement a proper application factory pattern where models are defined separately, and ensure blueprints are correctly registered without import conflicts.

- [x] **Complete Blueprint Implementation**  
  Properly implement the sentiment blueprint that is currently disabled. Restructure the code to avoid circular imports while maintaining the modular architecture intended with the blueprint design.

- [x] **Implement Application Configuration**  
  Move hardcoded configuration from app.py to a config.py module with different environment configurations. Separate development, testing, and production settings to make the application more maintainable and deployable.

## Code Quality

- [ ] **Implement Error Handling**  
  Replace bare except blocks in sentiment/ml.py with specific exception handling. Add proper error responses with appropriate HTTP status codes for API endpoints to improve debugging and user experience.

- [x] **Add Testing Infrastructure**  
  Create a comprehensive test suite with pytest fixtures for both unit and integration tests. Focus on integration testing to ensure the API endpoints are working as expected, and that the correct data is being passed to the frontend. Ensure that the test suite is comprehensive and covers all functionality. Ensure that the test suite is easy to run and that the tests are fast to run. Ensure that this works with github's CI tooling. 

- [x] **Modernize Dependencies**  
  Update requirements.txt to include specific version numbers and add missing dependencies like tensorflow. Consider using Poetry or Pipenv for better dependency management and reproducible environments.

## Security

- [ ] **Secure Static Asset References**  
  Fix relative paths in templates/base.html that may break in subdirectories. Use Flask's url_for() function for all static asset references to ensure they work correctly across the application.

- [ ] **Implement API Security**  
  Add CSRF protection and input validation on API endpoints in sentiment/views.py. Implement rate limiting and consider adding authentication for any sensitive operations to protect against abuse.

## Frontend

- [x] **Organize Frontend Assets**  
  Implement a proper frontend build process with minification and bundling. Ideally, fully commit to Elm architecture throughout more of the application. If Elm is lacking key features, then JS libraries should be used.

## Performance

- [ ] **Optimize Model Loading**  
  Move the SentimentModel initialization out of the request path in views.py to avoid initializing for each request. Implement a caching strategy for model predictions to reduce computation time for repeated inputs.