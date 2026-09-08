FROM python:3.11-slim

WORKDIR /app

# Install system utilities and ffmpeg for audio file processing.
RUN apt-get update && apt-get install -y --no-install-recommends \
		build-essential \
		ffmpeg \
		curl \
		&& rm -rf /var/lib/apt/lists/*

# Install Python dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code.
COPY . .

# Expose standard Flask API port.
EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
	CMD curl -f http://localhost:5000/api/health || exit 1

CMD ["python", "app.py"]
