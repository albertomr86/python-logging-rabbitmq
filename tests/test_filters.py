import pytest
from logging import makeLogRecord
from python_logging_rabbitmq.filters import FieldFilter


class TestFieldFilter:
  @pytest.fixture
  def record(self):
    return makeLogRecord({
      "relativeCreated": 280.61580657958984,
      "process": 13105,
      "args": [],
      "module":  "test",
      "funcName": "<module>",
      "host": "albertomr86-laptop",
      "exc_text": None,
      "name": "myapp",
      "thread": 140032818181888,
      "created": 1482290387.454017,
      "threadName": "MainThread",
      "msecs": 454.01692390441895,
      "filename": "test.py",
      "levelno": 10,
      "processName": "MainProcess",
      "pathname": "test.py",
      "lineno": 11,
      "msg": "test debug",
      "exc_info": None,
      "levelname": "DEBUG"
    })

  def test_no_fields_at_root_level(self, record):
    expected_len = len(record.__dict__)

    filter = FieldFilter({}, True)
    filter.filter(record)

    assert expected_len == len(record.__dict__)

  def test_fields_at_root_level(self, record):
    fields = {
      'locale': 'en-US',
      'activated': True
    }

    filter = FieldFilter(fields, True)
    filter.filter(record)
    updated_record = record.__dict__

    assert 'locale' in updated_record
    assert 'activated' in updated_record
    assert 'fields' not in updated_record

  def test_empty_group_of_fields(self, record):
    expected_len = len(record.__dict__) + 1

    filter = FieldFilter({}, False)
    filter.filter(record)
    updated_record = record.__dict__

    assert expected_len == len(updated_record)
    assert 'fields' in updated_record
    assert 0 == len(updated_record['fields'])

  def test_group_of_fields(self, record):
    fields = {
      'locale': 'en-US',
      'activated': True
    }

    filter = FieldFilter(fields, False)
    filter.filter(record)
    updated_record = record.__dict__

    assert 'locale' not in updated_record
    assert 'activated' not in updated_record
    assert 'fields' in updated_record

    assert isinstance(updated_record['fields'], dict)
    assert 'locale' in updated_record['fields']
    assert 'activated' in updated_record['fields']
