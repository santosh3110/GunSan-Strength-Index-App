FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PORT=7860
EXPOSE 7860

CMD exec gunicorn app:app --workers 2 --threads 8 --timeout 120 --bind 0.0.0.0:$PORT