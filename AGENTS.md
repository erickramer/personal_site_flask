# Agent Instructions

## Running Tests

- Backend tests use `pytest`. Run them with:
  ```bash
  make test-backend
  # or
  python -m pytest
  ```
- To run the full suite including frontend tests, use:
  ```bash
  make test-all
  ```
  (Requires Node.js and Elm.)

## Code Change Policy

- **Every code change must include appropriate tests.**
- **All tests must pass before completing a task.** Run the test commands above and ensure they succeed.
- If any test fails, fix the failing tests before finalizing the work.
