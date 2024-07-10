from fastapi import FastAPI

from .routers import router

from .instrumentation import instrument

app = FastAPI()
app.include_router(router)

# instrument(app)