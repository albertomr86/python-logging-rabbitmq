# coding: utf-8
# Thanks to https://github.com/lobziik/rlog
import sys

if sys.version_info[0] == 2:
    text_type = unicode
    from Queue import Queue as Queue
else:
    text_type = str
    from queue import Queue as Queue

try:
    import ujson as json  # noqa: F401
except ImportError:
    import json  # noqa: F401

# Support for Django.
try:
    from django.core.serializers.json import DjangoJSONEncoder as JSONEncoder  # noqa: F401
    from django.views.debug import ExceptionReporter as ExceptionReporter   # noqa: F401
except:
    from json.encoder import JSONEncoder as JSONEncoder  # noqa: F401
    ExceptionReporter = None
