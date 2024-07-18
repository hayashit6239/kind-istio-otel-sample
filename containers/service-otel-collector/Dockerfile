FROM otel/opentelemetry-collector-contrib:0.90.1

COPY ./containers/service-otel-collector/otel-collector.yml /etc/otel-collector.yml

CMD ["--config=/etc/otel-collector.yml"]