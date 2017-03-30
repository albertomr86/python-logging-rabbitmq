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
