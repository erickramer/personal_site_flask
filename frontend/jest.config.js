module.exports = {
  // The test environment that will be used for testing
  testEnvironment: 'jsdom',
  
  // The glob patterns Jest uses to detect test files
  testMatch: [
    '**/__tests__/**/*.js',
    '**/?(*.)+(spec|test).js'
  ],
  
  // An array of file extensions your modules use
  moduleFileExtensions: ['js', 'json'],
  
  // Transform files with babel-jest
  transform: {
    '^.+\\.js$': 'babel-jest',
  },
  
  // Handle CSS/image imports in tests
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/__mocks__/fileMock.js'
  },
  
  // Setup files to run before tests
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  
  // Code coverage configuration
  collectCoverageFrom: [
    'src/js/**/*.js',
    '!**/node_modules/**',
    '!**/vendor/**'
  ],
  
  // The directory where Jest should output coverage files
  coverageDirectory: 'coverage',
  
  // Automatically clear mock calls and instances between tests
  clearMocks: true,
};