# Use an official Python runtime as a parent image
FROM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 6464 available to the world outside this container
EXPOSE 6464

# Define environment variables
ENV HOST=0.0.0.0
ENV PORT=6464

# Set the PYTHONPATH environment variable
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Run main.py when the container launches
CMD ["python", "/app/src/main.py"]
# CMD ["python", "./src/main.py"]