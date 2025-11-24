FROM python:3.11-slim

# --- install system deps (chrome) ---
RUN apt-get update && apt-get install -y \
    wget gnupg2 ca-certificates unzip curl xvfb \
    fonts-liberation libnss3 libgconf-2-4 libx11-xcb1 libxcomposite1 libxcursor1 \
    libxdamage1 libxi6 libxtst6 libatk-bridge2.0-0 libgtk-3-0 libasound2 \
  && rm -rf /var/lib/apt/lists/*
# Install Chrome (stable)
RUN wget -q -O /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
 && apt-get update && apt-get install -y /tmp/google-chrome-stable_current_amd64.deb || apt-get -f install -y \
 && rm -f /tmp/google-chrome-stable_current_amd64.deb \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .
# create necessary directories
RUN mkdir -p /app/downloads /app/logs
# set environment variables
ENV PYTHONUNBUFFERED=1
# expose api port
EXPOSE 5000

# default command runs gunicorn for API
CMD ["gunicorn", "api.json_api_server:app", "-b", "0.0.0.0:5000", "--workers", "1", "--threads", "4"]