import logging


class FieldFilter(logging.Filter):
    """
    Filter to add extra fields before log the record.
    @alternative: https://docs.python.org/2/library/logging.html#loggeradapter-objects
    """

    def __init__(self, fields, fields_under_root):
        super(FieldFilter, self).__init__()

        self.fields = fields if isinstance(fields, dict) else {}
        self.fields_under_root = fields_under_root

    def filter(self, record):
        if self.fields_under_root:
            for field in self.fields:
                setattr(record, field, self.fields[field])
        else:
            setattr(record, 'fields', self.fields)

        return True
