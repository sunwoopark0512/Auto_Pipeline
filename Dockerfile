FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SLACK_TOKEN="your-slack-token"

CMD ["python", "run_pipeline.py"]
