from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from . import functions
from .database import get_db
from .schemas import Author, Book, BookDetails
from .instrumentation import parse_trace

from opentelemetry import trace, metrics
import logging
import time
from opentelemetry.propagate import extract

router = APIRouter()
tracer = trace.get_tracer_provider().get_tracer("book-service-b")
logger = logging.getLogger()
meter = metrics.get_meter(__name__)

routers_counter = meter.create_counter(
    "routers.count",
    unit="1"
)

routers_duration_histogram = meter.create_histogram(
    "routers.duration",
    unit="ms"
)


@router.post("/books", tags=["/books"])
async def add_book(name: str, author_id: int, db: AsyncSession = Depends(get_db)) -> Book:
    # with trace.get_tracer_provider().get_tracer("book-service").start_as_current_span(__name__) as span:
    book = await functions.add_book(name, author_id, db)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return Book.model_validate(book)

@router.get("/books", tags=["/books"])
async def get_books(request: Request, db: AsyncSession = Depends(get_db)) -> list[Book]:
    books = await functions.get_books(db)
    res = list(map(Book.model_validate, books))
    return res

@router.get("/books/{book_id}", tags=["/books"])
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)) -> Book:
    book = await functions.get_book(book_id, db)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
    return Book.model_validate(book)


@router.get("/books/{book_id}/details", tags=["/books"])
async def book_details(book_id: int, db: AsyncSession = Depends(get_db)) -> BookDetails:
    book = await functions.book_details(book_id, db)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
    return BookDetails.model_validate(book)


# @router.put("/authors", tags=["/authors"])
# async def update_author(author_id: int, name: str, db: AsyncSession = Depends(get_db)) -> Author:
#     author = await functions.update_author(author_id, name, db)
#     if author is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
#     return Author.model_validate(author)


@router.put("/books", tags=["/books"])
async def update_book(book_id: int, name: str, db: AsyncSession = Depends(get_db)) -> Book:
    book = await functions.update_book(book_id, name, db)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
    return Book.model_validate(book)


# @router.delete("/authors", tags=["/authors"])
# async def delete_author(author_id: int, db: AsyncSession = Depends(get_db)):
#     ok = await functions.delete_author(author_id, db)
#     if not ok:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")

@router.delete("/books", tags=["/books"])
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    ok = await functions.delete_book(book_id, db)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")

@router.post("/micro/b", tags=["/micro"])
async def test_micro(request: Request, db: AsyncSession = Depends(get_db)):
    logger.info(request)
    context = extract(request.headers)
    with tracer.start_as_current_span(__name__, context=context) as span:
        book = await functions.add_book("micro連携2", 1, db)
        if book is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
        return Book.model_validate(book)