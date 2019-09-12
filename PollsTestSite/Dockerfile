FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt

LABEL "com.datadoghq.ad.logs"='[{"source":"Django", "service": "webapp" }]'
