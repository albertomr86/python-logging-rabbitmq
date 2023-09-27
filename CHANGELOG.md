# v2.3.0 (2023-09-27)

### Features

- PR#24 : Added the option `remove_request` to decide whether the request's properties are removed from the record to log. (Thank you [@donbowman](https://github.com/donbowman))

### Fixes

- PR#37 : Call `task_done()` to complete the item dequeued. Reported by PR#32 PR#31, and PR#30.


# v2.2.0 (2022-04-24)

### Features

- PR#25 Handling thread shutdown (Thanks to [@donbowman](https://github.com/donbowman)).


# v2.1.0 (2022-04-23)

### Features

- PR#19 Heartbeat.
- PR#26 Put messages in the queue with a specific content type.

### Fixes

- PR#27 Minor corrections in the documentation.


# v2.0.0 (2019-06-26)

### Fixes

- PR#14 Heartbeat interval

# v1.1.1 (2019-03-10)

### Features

- Integration with [Travis CI](https://travis-ci.org/).
- Configuration for tests. Using [pipenv](https://github.com/pypa/pipenv).
- PR#10 Support for `pika` > 0.10.

### Fixes

- Removed direct dependency with Django.
- PR#11 The log record was being formatted twice.


# v1.0.9 (2018-05-04)

### Fixes

- PR#7 Fixed `exchange_type` parameter in `channel.exchange_declare` (Thanks to [@cklos](https://github.com/cklos)).


# v1.0.8 (2018-03-22)

### Features

- PR#6 Allow message headers when publishing to the queue (Thanks to [@merretbuurman](https://github.com/merretbuurman)).


# v1.0.7 (2017-05-15)

### Features

- Added support to customize the `routing_key` (Thanks to [@hansyulian](https://github.com/hansyulian)).


# v1.0.6 (2017-03-29)

### Fixes

- PR#3, PR#4 Fix compatibility with python3 in `RabbitMQHandlerOneWay` (by [@sactre](https://github.com/sactre)).


# v1.0.5 (2017-03-28)

### Chrores

- Explicit local imports.


# v1.0.4 (2017-03-15)

### Features

- PR#1 Added new handler `RabbitMQHandlerOneWay` (by [@wallezhang](https://github.com/wallezhang)). 


# v1.0.3 (2017-03-13)

- Added config parameter `close_after_emit`. Close connection after emit the record.


# v1.0.2 (2016-12-23)

### Features

- Expose `JSONFormatter`.


# v1.0.1 (2016-12-21)

Minor corrections in the documentation.


# v1.0.0 (2016-12-21)

First release.

