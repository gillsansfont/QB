FROM python:3.10-slim

WORKDIR /app

# 1) Install git so pip can clone GitHub repos
RUN apt-get update \
 && apt-get install -y git \
 && rm -rf /var/lib/apt/lists/*

# 2) Copy & install requirements (including QuantumBlur from GitHub)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copy your application code
COPY app.py .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
