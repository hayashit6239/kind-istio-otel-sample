from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import functions
from .database import get_db
from .schemas import Author, Book, BookDetails

from opentelemetry import trace, metrics
import logging
import time

router = APIRouter()
tracer = trace.get_tracer_provider().get_tracer("book-servic-a")
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

@router.post("/authors", tags=["/authors"])
async def add_author(name: str, db: AsyncSession = Depends(get_db)) -> Author:
    author = await functions.add_author(name, db)
    return Author.model_validate(author)


# @router.post("/books", tags=["/books"])
# async def add_book(name: str, author_id: int, db: AsyncSession = Depends(get_db)) -> Book:
#     # with trace.get_tracer_provider().get_tracer("book-service").start_as_current_span(__name__) as span:
#     book = await functions.add_book(name, author_id, db)
#     if book is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
#     return Book.model_validate(book)


@router.get("/authors", tags=["/authors"])
async def get_authors(db: AsyncSession = Depends(get_db)) -> list[Author]:
    routers_counter.add(1, {
        "routers.type": "GET_AUTHORS"
    })
    with tracer.start_as_current_span(__name__) as span:
        start_time = time.monotonic()

        span.add_event(name="get_authors")
        authors = await functions.get_authors(db)
        res = list(map(Author.model_validate, authors))

        end_time = time.monotonic()

        duration_ms = (end_time - start_time) * 1000
        routers_duration_histogram.record(
            duration_ms,
            attributes={
                "routers.type": "GET_AUTHORS"
            }
        )
        return res


# @router.get("/books", tags=["/books"])
# async def get_books(db: AsyncSession = Depends(get_db)) -> list[Book]:
#     routers_counter.add(1, {
#         "routers.type": "GET_BOOKS"
#     })
#     logger.info("out of src.routers span")
#     with tracer.start_as_current_span(__name__) as span:
#         start_time = time.monotonic()

#         logger.info("in src.routers span start")
#         span.add_event(name="get_books")
#         books = await functions.get_books(db)
#         res = list(map(Book.model_validate, books))

#         end_time = time.monotonic()

#         duration_ms = (end_time - start_time) * 1000
#         routers_duration_histogram.record(
#             duration_ms,
#             attributes={
#                 "routers.type": "GET_BOOKS"
#             }
#         )
#         logger.info("in src.routers span end")
#     return res


@router.get("/authors/{author_id}", tags=["/authors"])
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)) -> Author:
    author = await functions.get_author(author_id, db)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return Author.model_validate(author)


# @router.get("/books/{book_id}", tags=["/books"])
# async def get_book(book_id: int, db: AsyncSession = Depends(get_db)) -> Book:
#     book = await functions.get_book(book_id, db)
#     if book is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
#     return Book.model_validate(book)


# @router.get("/books/{book_id}/details", tags=["/books"])
# async def book_details(book_id: int, db: AsyncSession = Depends(get_db)) -> BookDetails:
#     book = await functions.book_details(book_id, db)
#     if book is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
#     return BookDetails.model_validate(book)


@router.put("/authors", tags=["/authors"])
async def update_author(author_id: int, name: str, db: AsyncSession = Depends(get_db)) -> Author:
    author = await functions.update_author(author_id, name, db)
    if author is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return Author.model_validate(author)


# @router.put("/books", tags=["/books"])
# async def update_book(book_id: int, name: str, db: AsyncSession = Depends(get_db)) -> Book:
#     book = await functions.update_book(book_id, name, db)
#     if book is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")
#     return Book.model_validate(book)


@router.delete("/authors", tags=["/authors"])
async def delete_author(author_id: int, db: AsyncSession = Depends(get_db)):
    ok = await functions.delete_author(author_id, db)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")


# @router.delete("/books", tags=["/books"])
# async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
#     ok = await functions.delete_book(book_id, db)
#     if not ok:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown book_id")

@router.get("/micro/a", tags=["/micro"])
async def test_micro(db: AsyncSession = Depends(get_db)):
    book = await functions.test_micro()
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Unknown author_id")
    return True
