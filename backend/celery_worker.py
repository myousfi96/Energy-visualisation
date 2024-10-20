from celery import Celery
from app import fetch_price, send_alert, price_threshold
from datetime import datetime

celery_app = Celery('celery_worker', broker='amqp://guest@rabbitmq//')

@celery_app.task
def monitor_price():
    price = asyncio.run(fetch_price())
    if price < price_threshold:
        message = f"Price {price} dropped below threshold {price_threshold} at {datetime.now()}"
        send_alert(message)