FROM python:3.9.16-bullseye

WORKDIR /app

# Install requirements
COPY requirements-base.txt requirements-base.txt
RUN pip3 install  --no-cache-dir --upgrade -r requirements-base.txt
COPY . .

RUN wget -q https://deb.nodesource.com/setup_19.x > /dev/null 2>&1
RUN bash ./setup_19.x > /dev/null 2>&1
RUN apt -qq install -y nodejs
RUN echo "Installed NodeJS"
WORKDIR /app/preordain/static/preordain
RUN npm install
RUN npm run build
WORKDIR /app
ARG API_PORT=8000

# hypercorn preordain.main:app
ENTRYPOINT [ "python3", "-m", "hypercorn", "preordain.main:app", "--bind", "0.0.0.0:8000"]
