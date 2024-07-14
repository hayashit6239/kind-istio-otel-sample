from fastapi import APIRouter, Depends, HTTPException, status

from . import gateways
from .schemas import Author, Book

router = APIRouter()


@router.get("/micro", tags=["/micro"])
async def test_micro():
    result = await gateways.get_authors_service_backend_a()
    result = await gateways.get_books_service_backend_b()
    return True


@router.get("/micro/authors", tags=["/micro/authors"])
async def get_authors() -> list[Author]:
    result = await gateways.get_authors_service_backend_a()
    return result


@router.get("/micro/books", tags=["/micro/books"])
async def get_books() -> list[Book]:
    result = await gateways.get_books_service_backend_b()
    return result
