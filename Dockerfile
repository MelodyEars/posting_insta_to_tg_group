FROM python:3.11.4-alpine3.18

WORKDIR /app

COPY requirements.txt .

RUN pip install aiogram --pre

RUN pip install -r requirements.txt

COPY . .

# Install necessary dependencies for Chromium
RUN apk update && apk add --no-cache \
    ca-certificates \
    curl \
    gnupg

# Install Chromium
RUN apk add --no-cache chromium

CMD ["python", "run.py"]

