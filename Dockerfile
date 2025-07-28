FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY approach_explanation.md .

CMD ["python", "./src/main.py", "--input-json", "/data/input.json", "--output-json", "/data/output.json"]