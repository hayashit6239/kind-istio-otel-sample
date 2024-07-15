from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .database import Author, Book

from opentelemetry import trace
import logging
import time

import requests, json

tracer = trace.get_tracer_provider().get_tracer("book-service-b")
logger = logging.getLogger()

async def add_author(name: str, db: AsyncSession) -> Author:
    author = Author(id=None, name=name, books=[])  # type: ignore
    db.add(author)
    await db.commit()
    await db.refresh(author)
    return author


async def add_book(name: str, author_id: int, db: AsyncSession) -> Book | None:
    author = await get_author(author_id, db)
    if not author:
        return None
    book = Book(id=None, name=name, author_id=author.id, author=author)  # type: ignore
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book


async def get_authors(db: AsyncSession):
    with tracer.start_as_current_span(__name__) as span:
        span.add_event(name="get_authors")
        return await db.scalars(select(Author))


async def get_books(db: AsyncSession):
    with tracer.start_as_current_span(__name__) as span:
        span.add_event(
            name="select all books",
            timestamp=int(time.time()),
            attributes={
                "sql": "select * from book"
            }
        )
        return await db.scalars(select(Book))


async def get_author(author_id: int, db: AsyncSession) -> Author | None:
    return await db.get(Author, author_id)


async def get_book(book_id: int, db: AsyncSession) -> Book | None:
    return await db.get(Book, book_id)


async def book_details(book_id: int, db: AsyncSession) -> Book | None:
    return await db.scalar(
        select(Book).where(Book.id == book_id).options(selectinload(Book.author))
    )


async def update_author(author_id: int, name: str, db: AsyncSession) -> Author | None:
    author = await db.get(Author, author_id)
    if author:
        author.name = name
        await db.commit()
        await db.refresh(author)
    return author


async def update_book(book_id: int, name: str, db: AsyncSession) -> Book | None:
    book = await db.get(Book, book_id)
    if book:
        book.name = name
        await db.commit()
        await db.refresh(book)
    return book


async def delete_author(author_id: int, db: AsyncSession) -> bool:
    author = await db.get(Author, author_id)
    if author is None:
        return False
    await db.delete(author)
    await db.commit()
    return True


async def delete_book(book_id: int, db: AsyncSession) -> bool:
    book = await db.get(Book, book_id)
    if book is None:
        return False
    await db.delete(book)
    await db.commit()
    return True

async def test_micro():
    with tracer.start_as_current_span(__name__) as span:
        logger.info("REGIST SERVIRCE BACKEND B")
        span.add_event(
            name="first service",
            timestamp=int(time.time()),
            attributes={
                "point": "first"
            }
        )
        return await db.scalars(select(Book))