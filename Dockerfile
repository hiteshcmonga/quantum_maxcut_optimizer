FROM python:3.10-slim

# Set working directory to /app/src
WORKDIR /app/src

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy code and data
COPY src/ /app/src
COPY data/ /app/data

EXPOSE 8000

# Run like you do locally: from inside src
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
