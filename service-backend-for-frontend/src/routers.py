from fastapi import APIRouter, Depends, HTTPException, status
import logging

from . import gateways
from .schemas import Author, Book

router = APIRouter()
logger = logging.getLogger()


@router.get("/micro", tags=["/micro"])
async def test_micro():
    logger.info("START GET MICRO SERVICE")
    result = await gateways.get_authors_service_backend_a()
    result = await gateways.get_books_service_backend_b()
    return True


@router.get("/micro/authors", tags=["/micro/authors"])
async def get_authors() -> list[Author]:
    result = await gateways.get_authors_service_backend_a()
    return result


@router.get("/micro/books", tags=["/micro/books"])
async def get_books() -> list[Book]:
    logger.info("START GET_BOOKS")
    result = await gateways.get_books_service_backend_b()
    return result
