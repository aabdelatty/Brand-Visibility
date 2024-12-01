# Use a slim Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app


# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its browser dependencies
RUN playwright install 

# Copy the backend code into the container
COPY . .

# Expose the port for FastAPI
EXPOSE ${BACKEND_PORT}


# Default command to initialize vector store and run FastAPI server
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${BACKEND_PORT}"]
