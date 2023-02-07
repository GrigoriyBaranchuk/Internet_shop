from celery import shared_task
import logging
import time
logger = logging.getLogger(__name__)


@shared_task
def add_some_product_to_admin_basket():
    time.sleep(20)
    logger.info('test info logs')
    logger.error('test error logs')
    logger.warning('test warning logs')
    logger.debug('test debug logs')

