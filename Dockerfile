# Use official Python image from DockerHub
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV DB_HOST=3.230.28.178
ENV DB_PORT=8002
ENV DB_NAME=mysql
ENV DB_USER=root
ENV DB_PASSWORD=utec

# Copy the rest of the app code to the container
COPY . .

# Expose the port on which the FastAPI app will run
EXPOSE 8001

# Command to run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

