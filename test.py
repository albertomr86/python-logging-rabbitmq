import logging
from python_logging_rabbitmq import RabbitMQHandler

logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)
logger.addHandler(RabbitMQHandler(host='192.168.99.100', port=5672))

logger.info('test info')
