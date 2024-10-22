import asyncio
import logging
from confluent_kafka import Consumer, KafkaException
from fastapi import BackgroundTasks
from app.config.kafka_config import KafkaConfig
from app.services.email_sender import send_email

logger = logging.getLogger(__name__)


def create_kafka_consumer():
    return Consumer(
        {
            "bootstrap.servers": KafkaConfig.BOOTSTRAP_SERVERS,
            "group.id": KafkaConfig.GROUP_ID,
            "auto.offset.reset": KafkaConfig.AUTO_OFFSET_RESET,
            'session.timeout.ms': 60000,  # Increase the session timeout to 60 seconds
            'max.poll.interval.ms': 300000,  # Increase the max poll interval to 5 minutes
        }
    )


async def consume_messages(background_tasks: BackgroundTasks):
    consumer = create_kafka_consumer()
    consumer.subscribe([KafkaConfig.TOPIC])

    print('Subscribed to topic: '+KafkaConfig.TOPIC)

    try:
        while True:
            try:
                msg = consumer.poll(1.0)  # Poll the message with a timeout of 1 second
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())

                # Log the raw message to see what we're receiving
                print('Raw message received: Check logs')
                logger.info(f"Raw message received: key={msg.key()}, value={msg.value()}")
                # Decode and process the message
                message_value = msg.value()
                if message_value is not None:
                    notification_data = message_value.decode('utf-8')  # Decode the message

                    logger.info(f"Decoded message to send_email: {notification_data}")

                    # Trigger background task for sending email
                    # asyncio.create_task(send_email(notification_data))
                    asyncio.run_coroutine_threadsafe(send_email(notification_data), asyncio.get_event_loop())
                else:
                    logger.warning("Received message with no value.")
            except KafkaException as e:
                logger.error(f"Kafka error: {e}")
            except Exception as e:
                logger.error(f"General error while consuming messages: {e}")
    finally:
        consumer.close()
        logger.info("Kafka consumer closed.")