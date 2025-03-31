# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

COPY requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy files
COPY . .

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "run.py"]
