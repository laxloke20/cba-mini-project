FROM python:3.9-slim

WORKDIR /app

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install dependencies without cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the code
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]