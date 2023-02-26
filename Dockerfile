FROM python:3.10

WORKDIR /preordain
COPY requirements-base.txt requirements-base.txt
RUN pip3 install  --no-cache-dir --upgrade -r requirements-base.txt
COPY . .

WORKDIR /
# install cron
RUN apt-get update && apt-get install cron -y -qq

# create two test applications that we will launch using cron
# RUN mkdir /app1 && echo 'echo `date +"%H:%M:%S"` - This is sample application 1!' > /app1/test.sh && chmod +x /app1/test.sh

# register cron jobs to start the applications and redirects their stdout/stderr
# to the stdout/stderr of the entry process by adding lines to /etc/crontab
# RUN echo "*/1 * * * * root /app1/test.sh > /proc/1/fd/1 2>/proc/1/fd/2" >> /etc/crontab

# start cron in foreground (don't fork)
WORKDIR /preordain
# ENTRYPOINT [ "cron", "-f" ]
CMD [ "python3", "-m", "hypercorn", "preordain.main:app", "--bind", "0.0.0.0:8000"]
