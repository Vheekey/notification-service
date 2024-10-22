import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks

from app.services.kafka_consumer import consume_messages
from routes import router as notification_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=logging.INFO,
                        filename='app.log',
                        filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    print("kafka consumer started")
    asyncio.create_task(consume_messages(background_tasks=BackgroundTasks()))
    yield
    print("Shutting down kafka consumer")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def health_check():
    return {"status": "running"}

app.include_router(notification_routes)
