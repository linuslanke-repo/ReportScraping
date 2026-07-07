FROM python:3.11-slim

# 2. Prevent Python from buffering logs
ENV PYTHONUNBUFFERED=1

# 3. Install required system tools and dependencies for headless browsing
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libatk-1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libext6 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libasound2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. Install Google Chrome for Testing and its matching ChromeDriver
RUN curl -sSL https://googleapis.com -o /tmp/chrome.zip \
    && unzip /tmp/chrome.zip -d /opt/ \
    && ln -s /opt/chrome-linux64/chrome /usr/local/bin/google-chrome \
    && curl -sSL https://googleapis.com -o /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /opt/ \
    && ln -s /opt/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && rm /tmp/chrome.zip /tmp/chromedriver.zip

# 5. Define workspace storage directory
WORKDIR /app

# 6. Build dependency caching layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 7. Transfer all local modules and directory structures
COPY . .

# 8. Expose Render tracking ports
EXPOSE 8080

# 9. Start the automation daemon loop
CMD ["python", "main.py"]
