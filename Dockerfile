# 1. Use a pre-configured Selenium container image that includes Python 3, Chrome, and WebDriver
FROM selenium/standalone-chrome:latest

# 2. Switch to root user temporarily to handle file paths and pip installations
USER root

# 3. Prevent Python from buffering console logs
ENV PYTHONUNBUFFERED=1

# 4. Define workspace storage directory
WORKDIR /app

# 5. Build dependency layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy all your local scripts and project files into the container
COPY . .

# 7. Expose Render tracking ports
EXPOSE 8080

# 8. Start the automation daemon loop
CMD ["python", "main.py"]
