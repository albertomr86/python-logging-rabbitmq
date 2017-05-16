# python-logging-rabbitmq
Logging handler to ships logs to RabbitMQ. Compatible with Django.

## Installation
Install using pip.
```sh
pip install python_logging_rabbitmq
```

## Handlers
This package has two built-in handlers that you can import as follows:
```python
from python_logging_rabbitmq import RabbitMQHandler
```

or (thanks to [@wallezhang](https://github.com/wallezhang))

```python
from python_logging_rabbitmq import RabbitMQHandlerOneWay
```

| Handler               | Description                                                                                                                                                                                                                                                                                  |
|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RabbitMQHandler       | Basic handler for sending logs to RabbitMQ. Every record will be delivered directly to RabbitMQ using the exchange configured.                                                                                                                                                               |
| RabbitMQHandlerOneWay | High throughput handler. Initializes an internal queue where logs are stored temporarily. A thread is used to deliver the logs to RabbitMQ using the exchange configured. Your app doesn't need to wait until the log is delivered. Notice that if the main thread dies you might lose logs. |

## Standalone python
To use with python first create a logger for your app, then create an instance of the handler and add it to the logger created.
```python
import logging
from python_logging_rabbitmq import RabbitMQHandler

logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)

rabbit = RabbitMQHandler(host='localhost', port=5672)
logger.addHandler(rabbit)

logger.debug('test debug')
```
As result, a similar message as follows will be sent to RabbitMQ:
```
{
   "relativeCreated":280.61580657958984,
   "process":13105,
   "args":[],
   "module":"test",
   "funcName":"<module>",
   "host":"UY-IT00150",
   "exc_text":null,
   "name":"myapp",
   "thread":140032818181888,
   "created":1482290387.454017,
   "threadName":"MainThread",
   "msecs":454.01692390441895,
   "filename":"test.py",
   "levelno":10,
   "processName":"MainProcess",
   "pathname":"test.py",
   "lineno":11,
   "msg":"test debug",
   "exc_info":null,
   "levelname":"DEBUG"
}
```

## Sending logs
By default, logs will be sent to RabbitMQ using the exchange **'log'**, this should be of **type topic**. The **routing key** used is formed by concatenating the *logger name* and the *log level*. For example:
```python
import logging
from python_logging_rabbitmq import RabbitMQHandler

logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)
logger.addHandler(RabbitMQHandler(host='localhost', port=5672))

logger.info('test info')
logger.debug('test debug')
logger.warn('test warning')
```
The messages will be sent using the following routing keys:
 - myapp.INFO
 - myapp.DEBUG
 - myapp.WARN

For an explanation about topics and routing keys go to https://www.rabbitmq.com/tutorials/tutorial-five-python.html

When create the handler, you're able to specify different parameters in order to connect to RabbitMQ or configure the handler behavior.

## Configuration
These are the configuration allowed:

| Parameter          | Description                                                                                                                              | Default                               |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------|
| host               | RabbitMQ Server hostname or ip address.                                                                                                  | localhost                             |
| port               | RabbitMQ Server port.                                                                                                                    | 5672                                  |
| username           | Username for authentication.                                                                                                             | None                                  |
| password           | Provide a password for the username.                                                                                                     | None                                  |
| exchange           | Name of the exchange to publish the logs. This exchange is considered of type topic.                                                     | log                                   |
| declare_exchange   | Whether or not to declare the exchange.                                                                                                  | False                                 |
| routing_key_format | Customize how messages are routed to the queues.                                                                                         | {name}.{level}                        |
| connection_params  | Allow extra params to connect with RabbitMQ.                                                                                             | None                                  |
| formatter          | Use custom formatter for the logs.                                                                                                       | python_logging_rabbitmq.JSONFormatter |
| close_after_emit   | Close the active connection after send a log. A new connection is open for the next log.                                                 | False                                 |
| fields             | Dict to add as a field in each logs send to RabbitMQ. This is useful when you want fields in each log but without pass them every time.  | None                                  |
| fields_under_root  | When is True, each key in parameter 'fields' will be added as an entry in the log, otherwise they will be logged under the key 'fields'. | True                                  |


### Examples
#### RabbitMQ Connection
```python
rabbit = RabbitMQHandler(
    host='localhost',
    port=5672,
    username='guest',
    password='guest',
    connection_params={
        'virtual_host': '/',
        'connection_attempts': 3,
        'socket_timeout': 5000
    }
)
```

#### Custom fields
```python
rabbit = RabbitMQHandler(
    host='localhost',
    port=5672,
    fields={
        'source': 'MyApp',
        'env': 'production'
    },
    fields_under_root=True
)
```

#### Custom formatter
By default, python_logging_rabbitmq implements a custom JSONFormatter; but if you prefer to format your own message you could do it as follow:

```python
import logging
from python_logging_rabbitmq import RabbitMQHandler

FORMAT = '%(asctime)-15s %(message)s'
formatter = logging.Formatter(fmt=FORMAT)
rabbit = RabbitMQHandler(formatter=formatter)
```
For a custom JSON Formatter take a look at https://github.com/madzak/python-json-logger

## Django
To use with Django add the handler in the [logging config](https://docs.djangoproject.com/en/1.9/topics/logging/#configuring-logging).

```
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
    'rabbit': {
        'level': 'DEBUG',
        'class': 'python_logging_rabbitmq.RabbitMQHandler',
        'host': 'localhost'
    }
  },
  'loggers': {
    'myapp': {
        'handlers': ['rabbit'],
        'level': 'DEBUG',
        'propagate': False
    }
  }
}
```

## Configuration
Same as when use it with standalone python, you could configure the handle directly when declaring it in the config:
```
LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
    'rabbit': {
        'level': 'DEBUG',
        'class': 'python_logging_rabbitmq.RabbitMQHandler',
        'host': 'localhost',
        'port': 5672,
        'username': 'guest',
        'password': 'guest',
        'exchange': 'log',
        'declare_exchange': False,
        'connection_params': {
            'virtual_host': '/',
            'connection_attempts': 3,
            'socket_timeout': 5000
        },
        'fields': {
            'source': 'MainAPI',
            'env': 'production'
        },
        'fields_under_root': True
    }
  },
  'loggers': {
    'myapp': {
        'handlers': ['rabbit'],
        'level': 'DEBUG',
        'propagate': False
    }
  }
}
```

#### Custom formatter
```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)-8s [%(asctime)s]: %(message)s',
        }
    },
    'handlers': {
        'rabbit': {
            'level': 'DEBUG',
            'class': 'python_logging_rabbitmq.RabbitMQHandler',
            'host': 'localhost',
            'formatter': 'standard'
        }
    },
    'loggers': {
        'myapp': {
            'handlers': ['rabbit'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
```

#### JSON formatter
```sh
pip install python-json-logger
```

```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'fmt': '%(name)s %(levelname) %(asctime)s %(message)s'
        }
    },
    'handlers': {
        'rabbit': {
            'level': 'DEBUG',
            'class': 'python_logging_rabbitmq.RabbitMQHandler',
            'host': 'localhost',
            'formatter': 'json'
        }
    },
    'loggers': {
        'myapp': {
            'handlers': ['rabbit'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
```

## Releases
| Date         | Version | Notes                                                    |
|--------------|---------|----------------------------------------------------------|
| May 15, 2017 | 1.0.7   | Adding support to customize the routing_key (Thanks to [@hansyulian](https://github.com/hansyulian)). |
| Mar 30, 2017 | 1.0.6   | Fix compatibility with python3 in RabbitMQHandlerOneWay (by [@sactre](https://github.com/sactre)). |
| Mar 28, 2017 | 1.0.5   | Explicit local imports.                                  |
| Mar 16, 2017 | 1.0.4   | Added new handler RabbitMQHandlerOneWay (by [@wallezhang](https://github.com/wallezhang)). |
| Mar 14, 2017 | 1.0.3   | Added config parameter close_after_emit.                 |
| Dec 21, 2016 | 1.0.2   | Minor fixes.                                             |
| Dec 21, 2016 | 1.0.1   | Minor fixes.                                             |
| Dec 21, 2016 | 1.0.0   | Initial release.                                         |

## What's next?
 - Let's talk about tests.
 - Issues, pull requests, suggestions are welcome.
 - Fork and improve it. Free for all.

## Similar efforts
 - MQHandler (https://github.com/ziXiong/MQHandler)
 - http://stackoverflow.com/a/25479008/2716524
 - LogBook (http://pydoc.net/Python/Logbook/0.12.5/logbook.queues/)
 - https://pypi.python.org/pypi/py-amqp-logging/0.1
