FROM python:3.9.16-bullseye

WORKDIR /app

# Install requirements
COPY requirements-base.txt requirements-base.txt
RUN pip3 install  --no-cache-dir --upgrade -r requirements-base.txt
COPY . .

ARG API_PORT=8000

# hypercorn preordain.main:app
ENTRYPOINT [ "python3", "-m", "hypercorn", "preordain.main:app", "--bind", $API_PORT]