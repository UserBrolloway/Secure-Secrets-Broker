import logging
from fastapi import FastAPI
from app.api import router
from app.database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Secure Secrets Broker", version="0.1.0")
app.include_router(router)

@app.on_event("startup")
def on_startup():
    logger.info("Initializing DB")
    init_db()
    logger.info("Startup complete")
