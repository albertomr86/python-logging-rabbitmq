from setuptools import setup, find_packages

setup(name='python-logging-rabbitmq',
      version='1.0.0',
      url='https://github.com/albertomr86/python-logging-rabbitmq',
      description='Send logs to RabbitMQ from Python/Django',
      author='Alberto Menendez Romero',
      author_email="albertomr86@gmail.com",
      license='MIT',
      install_requires=['pika==0.10.0'],
      packages=find_packages(),
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=True)
