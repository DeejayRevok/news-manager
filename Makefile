build_chart:
	cat VERSION | xargs -I {} helm package -u --version {} --app-version {} helm/news-manager

run_web_server:
	nohup metricbeat -e -c /etc/metricbeat/metricbeat.yml &
	nohup filebeat -e -c /etc/filebeat/filebeat.yml &
	python -m aiohttp.web -H 0.0.0.0 -P 8080 app.loaders.web_app_loader:load

run_kombu_event_consumer:
	nohup metricbeat -e -c /etc/metricbeat/metricbeat.yml &
	nohup filebeat -e -c /etc/filebeat/filebeat.yml &
	python app/kombu_event_consumer_runner.py -e $(EVENT_NAME) -c $(CONSUMER_NAME)

run_rpyc_query_engine:
	nohup metricbeat -e -c /etc/metricbeat/metricbeat.yml &
	nohup filebeat -e -c /etc/filebeat/filebeat.yml &
	python app/rpyc_query_engine_runner.py -ht 0.0.0.0 -q $(QUERY_NAME)
