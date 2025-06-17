# Use Python 3.9 slim image
FROM python:3.9-slim AS builder

WORKDIR /app

# Install system packages for building assets
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs npm curl && rm -rf /var/lib/apt/lists/*

# Install Elm globally for asset compilation
RUN npm install -g elm@0.19.1 elm-test@0.19.1-revision9

# Copy dependency files
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Build frontend and Elm assets
RUN make build-frontend && make build-elm

# Final runtime image
FROM python:3.9-slim
WORKDIR /app

# Copy installed packages and source from builder stage
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

ENV PORT=8080
EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "app:app"]
