# Use lightweight Python image
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Copy frontend static files
COPY . .

# Expose port
EXPOSE 8000

# Serve static files using Python
CMD ["python", "-m", "http.server", "8000", "--bind", "0.0.0.0"]
