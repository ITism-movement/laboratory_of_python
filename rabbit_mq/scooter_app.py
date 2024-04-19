import os

from rabbit_mq.sync_consumer import RabbitMQConsumer
import os

SERIAL_NUMBER = os.getenv("SCOOTER_SERIAL_NUMBER") or "1A"

if __name__ == "__main__":
    consumer = RabbitMQConsumer(
        consumer_tag=f'{SERIAL_NUMBER}_scooter',
        queue_name=SERIAL_NUMBER,
        auto_delete=True,
    )
    try:
        consumer.start_consuming()
    finally:
        consumer.close_connection()
