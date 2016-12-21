# coding: utf-8
import logging
from socket import gethostname
from compat import json
from compat import text_type


class JSONFormatter(logging.Formatter):
    """
    Formatter to convert LogRecord into JSON.
    Thanks to: https://github.com/lobziik/rlog
    """
    def format(self, record):
        data = record.__dict__.copy()

        if record.args:
            msg = record.msg % record.args
        else:
            msg = record.msg

        data.update(
            host=gethostname(),
            msg=msg,
            args=tuple(text_type(arg) for arg in record.args)
        )

        if 'exc_info' in data and data['exc_info']:
            data['exc_info'] = self.formatException(data['exc_info'])

        return json.dumps(data)
