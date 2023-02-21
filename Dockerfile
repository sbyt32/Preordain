# syntax=docker/dockerfile:1

FROM python:3.10
WORKDIR /pfs
COPY requirements-base.txt requirements-base.txt
RUN pip3 install  --no-cache-dir --upgrade -r requirements-base.txt
COPY . .
CMD [ "python3", "-m", "hypercorn", "preordain.main:app", "--bind", "0.0.0.0:8000"]
