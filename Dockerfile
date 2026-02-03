# Automated Certificate Mailer - Docker Container
# Build: docker build -t certificate-mailer .
# Run: docker run -v $(pwd)/certificates:/app/certificates certificate-mailer

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY send_emails2.py .
COPY update_students_csv.py .
COPY requirements.txt .

# Install dependencies (none required for this project)
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p certificates logs

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "send_emails2.py", "--help"]
