FROM python:3.10

# Install Chrome dependencies
RUN apt-get update && apt-get install -y wget gnupg2 curl unzip

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# Install Chromedriver
RUN apt-get install -y chromium-driver

# Set display port to avoid crashes
ENV DISPLAY=:99

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Run your app
CMD ["python", "app.py"]
