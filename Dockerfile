# Use the official Playwright Python image as a base
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# 1. Set the working directory inside the container
WORKDIR /app

# 2. Copy only the requirements first for caching
COPY requirements.txt .

# 3. Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Pre-install the SPECIFIC browser that solved our previous issues
# we must install the actual branded Google Chrome binary.
# 'playwright install' alone installs Chromium, Firefox, and WebKit.
# 'playwright install chrome' specifically adds the Google Chrome stable build.
RUN playwright install chrome

# 5. THE "PORTABILITY" LINE: Copy the project code into the image
COPY . .

# Default command: Runs the full production suite with reporting and tracing
CMD ["pytest", "--tracing", "retain-on-failure", "--browser_name", "chrome", "--html=report.html", "--self-contained-html", "test_attendance_bdd.py"]