# TODO Improvements

1. **Secure Static Asset References**
   Use `url_for()` for all static file references in templates such as `asteroids.html` instead of hard coded paths.
2. **Restrict Debug Routes**
   Expose the `/debug` endpoints only in development mode to avoid leaking information in production.
3. **Add Pre-commit Hooks**
   Configure a pre-commit setup for formatting and linting to keep code style consistent.
4. **Create Custom Error Pages**
   Add 404 and 500 error templates and register error handlers in `app.py`.
5. **Document Required Environment Variables**
   Expand the README with instructions for setting `SECRET_KEY` and other configuration values.
6. **Fix Truncated Documentation Files**
   Ensure files like `README.md` and `requirements.txt` end with a newline and contain complete content.
