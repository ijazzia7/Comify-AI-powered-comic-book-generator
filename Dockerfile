# Use lightweight Python image
FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Cloud Run expects the app to listen on $PORT
ENV PORT=8080

# Expose port (not strictly needed for Cloud Run, but good practice)
EXPOSE 8080

# Run Gunicorn (production WSGI server)
CMD ["gunicorn", "-b", ":8080", "app:app"]