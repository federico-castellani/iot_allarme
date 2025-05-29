.PHONY: start prepare stop

prepare:
	mkdir -p influxdb_data influxdb_config grafana_data
	@if [ -d grafana_data ]; then \
		owner=$$(stat -c "%u" grafana_data); \
		if [ "$$owner" -ne 472 ]; then \
			echo "Changing owner of grafana_data to 472"; \
			sudo chown -R 472:472 grafana_data; \
		fi \
	fi

start: prepare
	docker-compose up -d

stop:
	docker-compose down
