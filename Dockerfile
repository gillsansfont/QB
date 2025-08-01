# Use the slim Python image
FROM python:3.10-slim

WORKDIR /app

# 1) Install git (and clean up)
RUN apt-get update \
 && apt-get install -y git \
 && rm -rf /var/lib/apt/lists/*

# 2) Copy & install requirements (including the GitHub QuantumBlur package)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copy your app code
COPY app.py .

# 4) Expose port & set entrypoint
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
