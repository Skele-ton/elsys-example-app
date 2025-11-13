# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (to leverage caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Create storage directory (if not exists)
RUN mkdir -p storage

# Expose port for FastAPI
EXPOSE 8000

# Run app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
