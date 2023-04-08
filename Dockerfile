FROM python:slim

RUN apt-get update && apt-get upgrade -y

ENV PYTHONUNBUFFERED 1 PYTHONDONOTWRITEBYTECODE 1

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

CMD python manage.py runserver 0.0.0.0:8000