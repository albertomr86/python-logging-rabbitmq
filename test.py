import logging
from python_logging_rabbitmq import RabbitMQHandler

logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)

rabbit = RabbitMQHandler(host='localhost', port=5672, content_type='STRING')
logger.addHandler(rabbit)

logger.warning('test warning')
