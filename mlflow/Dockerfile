FROM python:3.11-slim

RUN pip install --no-cache-dir mlflow psycopg2-binary

WORKDIR /app

EXPOSE 5000

CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]
