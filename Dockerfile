FROM python:3.8-slim
COPY ./ /app/news_manager

WORKDIR /app

RUN apt-get update
RUN apt-get -y install gcc
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get install wget -y
RUN apt-get install gnupg -y
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -
RUN apt-get install apt-transport-https -y
RUN echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | tee -a /etc/apt/sources.list.d/elastic-7.x.list
RUN apt-get update
RUN apt-get install git -y
RUN apt-get install metricbeat=7.11.2

RUN pip install --upgrade pip
RUN pip install -r ./news_manager/requirements-prod.txt

COPY ./tools_config/metricbeat.yml /etc/metricbeat/metricbeat.yml

EXPOSE 8080
CMD service metricbeat start && export PYTHONPATH=${PYTHONPATH}:/app/news_manager && python ./news_manager/webapp/main.py -c ./news_manager/configs/config_docker.yml