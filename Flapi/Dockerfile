FROM python:3

ENV PYTHONUNBUFFERED 1
ENV export FLASK_APP=api.py
ENV export FLASK_RUN_PORT=8000
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt

LABEL "com.datadoghq.ad.logs"='[{"source":"Flask", "service": "Flapi" }]'
