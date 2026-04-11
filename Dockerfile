FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Install system dependencies + awscli
RUN apt-get update && \
    apt-get install -y awscli && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["python", "app.py"]