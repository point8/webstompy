**********************************************************************
webstompy: A simple Python STOMP implementation with WebSocket support
**********************************************************************

This is webstompy, your friendly Python STOMP interface with WebSocket support. Currently, it supports [version 1.1 of the STOMP specification](https://stomp.github.io/stomp-specification-1.1.html).

**Current release:** |version| (|today|)

*Note: webstompy may not be feature-complete or respect the STOMP specification in full detail. It merely suffices our requirements. In case you observe non-standard behavior or missing functionality, feel free to leave an issue in the tracker or provide a pull request.*

webstompy is aimed at simplicity of usage.

## Documentation

* 💾 `Code repository <https://github.com/point8/webstompy>`_
* This README file contains some basic documentation for installation and development.
* :books: **[Project documentation](https://webstompy.readthedocs.io)**
* :bug: **For bug reports and feature requests use the [issue tracker](https://github.com/point8/webstompy/issues)**

## Usage

Assuming you have a local RabbitMQ server with the Web STOMP Plugin running on port 15674 (see below how to set this up), the following example should work and produce a visible result:

```python
from websocket import create_connection
import webstompy

class MyListener(webstompy.StompListener):
    def on_message(self, frame):
        print('Listener caught this frame: ', frame.payload)

ws_echo = create_connection('ws://127.0.0.1:15674/stomp/websocket')

connection = webstompy.StompConnection(connector=ws_echo)
connection.add_listener(MyListener())
connection.connect(login='guest', passcode='guest')
connection.send(destination='/topic/test', message='hello queue a')
connection.subscribe(destination='/topic/test', id='0')
connection.send(destination='/topic/test', message='hello queue b')
```

### Logging

webstompy supports logging via the Python standard logging module. By default, it will just print the log levels `WARINING` and `ERROR`. You can control webstompy's logging in your app via

```python
import logging
logging.getLogger("webstompy").setLevel(logging.CRITICAL)
```

### Setup a local RabbitMQ demo

The above usage example can be realized using a RabbitMQ server with the [Web STOMP Plugin](https://www.rabbitmq.com/web-stomp.html). RabbitMQ acts as a broker, the example above in the end speaks with itself.

#### Install RabbitMQ with activated Web STOMP Plugin

Luckily, there is [beevelop/rabbitmq-stomp](https://hub.docker.com/r/beevelop/rabbitmq-stomp/), a Docker image for RabbitMQ with support for STOMP. Install it and run the RabbitMQ server:

```
docker pull beevelop/rabbitmq-stomp
docker run -d --name rabbit-stomp -p 15674:15674 beevelop/rabbitmq-stomp
```

Your RabbitMQ server WebSocket will listen on port 15674 and be available via <http://127.0.0.1:15674/stomp>.

## License

[MIT License](LICENSE), Copyright (c) 2020 Point 8 GmbH
