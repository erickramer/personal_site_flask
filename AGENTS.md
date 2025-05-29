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

## Additional Information for Codex

- Add any helpful notes here that could speed up future development.
  This could include undocumented details about how the repository works,
  useful bash commands, debugging tips, or anything else.
- You may create additional `AGENTS.md` files recursively in subdirectories of
  this repo if more targeted instructions would be beneficial.
