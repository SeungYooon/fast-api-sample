FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt start.sh /app/
COPY ./app /app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["./start.sh"]
