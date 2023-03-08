FROM python:3.9.16-bullseye

WORKDIR /app

RUN apt-get update && apt-get -y install cron


# Install requirements
COPY requirements.txt requirements.txt
RUN pip3 install  --no-cache-dir --upgrade -r requirements.txt
COPY . .

# load crontab data
RUN crontab /app/crontab

ENTRYPOINT ["tail", "-f", "/dev/null"]