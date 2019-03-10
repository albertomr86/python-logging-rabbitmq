import sys, os

lib = os.path.join(
  os.path.dirname(os.path.abspath(__file__)),
  '..',
  'python_logging_rabbitmq'
)

sys.path.append(os.path.realpath(lib))
