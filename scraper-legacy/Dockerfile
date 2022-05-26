
FROM python:3.8-buster

ENV TZ="Pacific/Auckland"

RUN apt-get update && apt-get -y install cron

COPY ./pisspricer-scraper /pisspricer-scraper
COPY ./requirements.txt .
COPY ./crontab .
COPY .env .

RUN python -m pip install  -r requirements.txt

RUN crontab crontab

# Create the log file to be able to run tail
RUN touch /var/log/logfile

CMD cron && tail -f /var/log/logfile
