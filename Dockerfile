# 1. Use an official stable Python 3 CPython runtime base image
FROM python:3.11-slim

# 2. Prevent Python from buffering stdout/stderr outputs (makes cloud logs appear instantly)
ENV PYTHONUNBUFFERED=1

# 3. Create and set the structural working directory inside the container
WORKDIR /app

# 4. Copy the requirements file first to take advantage of Docker caching
COPY requirements.txt .

# 5. Install the third-party scraping dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy ALL your project directories and scripts into the container workspace
# This accurately mirrors your entire VS Code directory tree structure inside the cloud
COPY . .

# 7. Explicitly expose port 8080 for incoming Render health checks
EXPOSE 8080

# 8. Set the execution trigger to launch our new coordinator script
CMD ["python", "main.py"]
