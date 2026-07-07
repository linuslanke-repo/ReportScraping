# 1. Start with a stable Linux Python base
FROM python:3.11-slim

# 2. Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# 3. Install Google Chrome and dependencies required for Linux headless browsing
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    && wget -q -O - https://google.com | apt-key add - \
    && sh -c 'echo "to [arch=amd64] http://google.com stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. Define workspace storage directory
WORKDIR /app

# 5. Build dependency caching layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Transfer all local modules and directory structures
COPY . .

# 7. Expose Render tracking ports
EXPOSE 8080

# 8. Start the automation daemon loop
CMD ["python", "main.py"]
