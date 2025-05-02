FROM python:3.9-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y cron
RUN apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY ./crontab /etc/cron.d/moki-crontab
RUN chmod 0644 /etc/cron.d/moki-crontab
RUN crontab /etc/cron.d/moki-crontab

RUN touch /app/cron.log

CMD cron && tail -f /app/cron.log