# -*- coding: utf-8 -*-
import logging
import pika
from pika import credentials
from formatters import JSONFormatter
from filters import FieldFilter


class RabbitMQHandler(logging.Handler):
    """
    Python/Django logging handler to ship logs to RabbitMQ.
    Inspired by: https://github.com/ziXiong/MQHandler
    """

    def __init__(self, level=logging.NOTSET, formatter=JSONFormatter(),
                 host='localhost', port=5672, connection_params=None,
                 username=None, password=None,
                 exchange='log', declare_exchange=False,
                 fields=None, fields_under_root=True):
        """
        Initialize the handler.

        :param level:             Logs level.
        :param formatter:         Use custom formatter for the logs.
        :param host:              RabbitMQ host. Default localhost
        :param port:              RabbitMQ Port. Default 5672
        :param connection_params: Allow extra params to connect with RabbitMQ.
        :param username:          Username in case of authentication.
        :param password:          Password for the username.
        :param exchange:          Send logs using this exchange.
        :param declare_exchange:  Whether or not to declare the exchange.
        :param fields:            Send these fields as part of all logs.
        :param fields_under_root: Merge the fields in the root object.
        """

        super(RabbitMQHandler, self).__init__(level=level)

        # Important instances/properties.
        self.exchange = exchange
        self.connection = None
        self.channel = None
        self.exchange_declared = not declare_exchange

        # Connection parameters.
        # Allow extra params when connect to RabbitMQ.
        # @see: http://pika.readthedocs.io/en/0.10.0/modules/parameters.html#pika.connection.ConnectionParameters
        conn_params = connection_params if isinstance(connection_params, dict) else {}
        self.connection_params = dict(conn_params.items() + dict(host=host, port=port, heartbeat_interval=0).items())

        if username and password:
            self.connection_params['credentials'] = credentials.PlainCredentials(username, password)

        # Logging.
        self.formatter = formatter
        self.fields = fields if isinstance(fields, dict) else {}
        self.fields_under_root = fields_under_root

        if len(self.fields) > 0:
            self.addFilter(FieldFilter(self.fields, self.fields_under_root))

        # Connect.
        self.createLock()
        self.open_connection()

    def open_connection(self):
        """
        Connect to RabbitMQ.
        """

        # Set logger for pika.
        # See if something went wrong connecting to RabbitMQ.
        handler = logging.StreamHandler()
        handler.setFormatter(self.formatter)
        rabbitmq_logger = logging.getLogger('pika')
        rabbitmq_logger.addHandler(handler)
        rabbitmq_logger.propagate = False
        rabbitmq_logger.setLevel(logging.WARNING)

        # Connect.
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(**self.connection_params))
        self.channel = self.connection.channel()

        if self.exchange_declared is False:
            self.channel.exchange_declare(exchange=self.exchange, type='topic', durable=True, auto_delete=False)
            self.exchange_declared = True

        # Manually remove logger to avoid shutdown message.
        rabbitmq_logger.removeHandler(handler)

    def emit(self, record):
        self.acquire()

        try:
            if not self.connection or not self.channel:
                self.open_connection()

            routing_key = "{name}.{level}".format(name=record.name, level=record.levelname)

            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=routing_key,
                body=self.format(record),
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )

        except Exception:
            self.channel, self.connection = None, None
            self.handleError(record)
        finally:
            self.release()

    def close(self):
        """
        Free resources.
        """

        self.acquire()

        try:
            if self.channel:
                self.channel.close()

            if self.connection:
                self.connection.close()
        finally:
            self.release()
