FROM fnndsc/python-poetry:latest

USER root
RUN apt-get update
RUN apt-get install -y curl

ENTRYPOINT cd /app && \
           poetry install && \
           poetry run python create_table.py && \
           poetry run uvicorn src.main:app --host 0.0.0.0 --reload --port 8082