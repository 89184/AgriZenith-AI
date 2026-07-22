FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (for pdfplumber, spacy, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose the port the API runs on
EXPOSE 8000

# Command to run the API
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]