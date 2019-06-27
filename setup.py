from setuptools import setup

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
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
]

INSTALL_REQUIRES = [
    'pika>=0.13'
]

TEST_REQUIRES = [
    "pytest>=4.3.0",
    "pytest-cov>=2.6.1",
    "pytest-mock>=1.10.1",
]

setup(name='python-logging-rabbitmq',
    version='2.0.0',

    url='https://github.com/albertomr86/python-logging-rabbitmq',
    description='Send logs to RabbitMQ from Python/Django',
    keywords='logging rabbitmq logs',
    license='MIT',

    author='Alberto Menendez Romero',
    author_email="albertomr86@gmail.com",

    classifiers=CLASSIFIERS,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",
    install_requires=INSTALL_REQUIRES,
    packages=['python_logging_rabbitmq'],
    extras_require={
        'dev': ['check-manifest']
    },

    setup_requires=['pytest-runner'],
    test_suite='tests',
    tests_require=TEST_REQUIRES,
    zip_safe=True)
