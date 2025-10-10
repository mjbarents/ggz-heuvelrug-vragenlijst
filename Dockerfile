FROM python:3.11-slim-bookworm

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .
RUN chown -R appuser:appuser /app

# Create instance directory for database
RUN mkdir -p instance && chown appuser:appuser instance

USER appuser

# Uses port 5000, change if .env sets a different port
CMD ["sh", "-c", "python init_db.py && gunicorn --bind 0.0.0.0:5000 --workers 1 app:app"]
