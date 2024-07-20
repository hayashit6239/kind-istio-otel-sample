from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from .routers import router

from .instrumentation import instrument

app = FastAPI()
app.include_router(router)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT") != "":
    instrument(app)