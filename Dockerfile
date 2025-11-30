FROM python:3.10-bullseye

# --- system deps ---
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl xvfb \
    fonts-liberation libnss3 libx11-xcb1 \
    libxcomposite1 libxcursor1 libxdamage1 \
    libxi6 libxtst6 libatk-bridge2.0-0 \
    libgtk-3-0 libasound2 libxrandr2 libxss1 libgbm1 \
    && rm -rf /var/lib/apt/lists/*

# --- install chrome ---
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google.list && \
    apt-get update && apt-get install -y google-chrome-stable

# --- install chromedriver ---
RUN CHROME_VERSION=$(google-chrome --version | sed 's/Google Chrome //') && \
    CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE") && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip

# --- install python deps ---
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "main.py"]