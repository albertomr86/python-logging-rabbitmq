# coding: utf-8
import logging
from socket import gethostname

from .compat import JSONEncoder
from .compat import json, text_type


class JSONFormatter(logging.Formatter):
    """
    Formatter to convert LogRecord into JSON.
    Thanks to: https://github.com/lobziik/rlog
    """
    def __init__(self, *args, **kwargs):
        include = kwargs.pop('include', None)
        exclude = kwargs.pop('exclude', None)
        super(JSONFormatter, self).__init__(*args, **kwargs)
        self.include = include
        self.exclude = exclude

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

        if self.include:
            data = {f: data[f] for f in self.include}
        elif self.exclude:
            for f in self.exclude:
                if f in data:
                    del data[f]

        return json.dumps(data, cls=JSONEncoder)
