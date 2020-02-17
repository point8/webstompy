import os
from setuptools import setup

exec(compile(open('webstompy/version.py', "rb").read(),
             'webstompy/version.py',
             'exec'))

setup(
    name='webstompy',
    description='A simple Python STOMP implementation with WebSocket support',
    url='https://github.com/point8/webstompy',
    author='Point 8 GmbH',
    author_email='kontakt@point-8.de',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=['webstompy', 'webstompy.transporter'],
    version=__version__,
    tests_require=['pytest', 'pytest-runner', 'pytest-cov'],
    setup_requires=['pytest-runner'],
    install_requires=['websocket-client']
)
