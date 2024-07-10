FROM fnndsc/python-poetry:latest

ENTRYPOINT cd /app && \
           poetry install && \
           poetry run python create_table.py && \
           poetry run uvicorn src.main:app --host 0.0.0.0 --reload --port 8080