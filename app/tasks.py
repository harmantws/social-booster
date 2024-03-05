# tasks.py
from celery import shared_task
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from .facebook_func import facebook_auto_post

logger = get_task_logger(__name__)

@shared_task
def schedule_facebook_post(session):
    try:
        # Extract date and time from the session
        publish_date = session.get("publish_date", "")
        publish_time = session.get("publish_time", "")

        # Combine date and time to create a datetime object
        scheduled_datetime = datetime.combine(publish_date, publish_time)

        # Schedule the post using Celery's apply_async with the eta argument
        schedule_facebook_postt.apply_async(args=[session], eta=scheduled_datetime)
        logger.info(f"Post scheduled for {scheduled_datetime}")

    except Exception as e:
        logger.error(f"Error scheduling post: {e}")
        raise

@shared_task
def schedule_facebook_postt(session):
    facebook_auto_post(session)
