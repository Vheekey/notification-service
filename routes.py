import logging

from fastapi import BackgroundTasks, APIRouter
from app.services.kafka_consumer import consume_messages

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/start-kafka-consumer")
def start_kafka_consumer(background_tasks: BackgroundTasks):
    background_tasks.add_task(consume_messages, background_tasks)
    return "Consumer started"