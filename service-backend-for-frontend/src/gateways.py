import requests, json
import logging
from typing import Callable

from opentelemetry.propagate import inject
from opentelemetry import trace

tracer = trace.get_tracer_provider().get_tracer("default")
logger = logging.getLogger()


async def get_service_backend_a_to_b():
    logger.info("REQUEST TO SERVICE BACKEND A TO SERVICE BACKEND B")
    func_name = f"{__name__}.get_service_backend_a_to_b"
    with tracer.start_as_current_span(func_name) as span:
        span.set_attribute("function.name", func_name)

        headers = {}
        inject(headers)
        url = "http://service-backend-a.default.svc.cluster.local:8081/micro/a"
        response = requests.get(
            url,
            headers=headers
        )
        return response.json()

async def get_authors_service_backend_a():
    logger.info("REQUEST TO SERVICE BACKEND A")
    func_name = f"{__name__}.get_authors_service_backend_a"
    with tracer.start_as_current_span(func_name) as span:
        # スパンに属性を追加する
        span.set_attribute("function.name", func_name)

        headers = {}
        inject(headers)
        url = "http://service-backend-a.default.svc.cluster.local:8081/authors"
        response = requests.get(
            url,
            headers=headers
        )
        return response.json()

async def get_books_service_backend_b():
    logger.info("REQUEST TO SERVICE BACKEND B")
    func_name = f"{__name__}.get_books_service_backend_b"
    with tracer.start_as_current_span(func_name) as span:
        # スパンに属性を追加する
        span.set_attribute("function.name", func_name)
        
        url = "http://service-backend-b.default.svc.cluster.local:8082/books"
        headers = {}
        inject(headers)
        response = requests.get(
            url,
            headers=headers
        )
        return response.json()