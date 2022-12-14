FROM python:3.10.7-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y netcat

CMD ["./startup.sh"]