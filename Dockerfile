FROM python:3.10-slim-bullseye
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y awscli && rm -rf /var/lib/apt/lists/*

RUN apt-get update && pip install -r requirements.txt
CMD ["python3", "app.py"]