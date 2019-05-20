FROM python:3.7
RUN apt-get update
ADD . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV="soa-shipping-microservice-docker"