from setuptools import setup, find_packages

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5'
]

INSTALL_REQUIRES = [
    'pika==0.10.0'
]

setup(name='python-logging-rabbitmq',
      version='1.0.2',

      url='https://github.com/albertomr86/python-logging-rabbitmq',
      description='Send logs to RabbitMQ from Python/Django',
      keywords='logging rabbitmq logs',
      license='MIT',

      author='Alberto Menendez Romero',
      author_email="albertomr86@gmail.com",

      classifiers=CLASSIFIERS,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages(),
      extras_require={
          'dev': ['check-manifest']
      },

      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=True)
