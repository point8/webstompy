"""webstompy logging service
"""

import logging


def get_logger(name="webstompy"):
    """Internal function to get logger for module

    This function returns a logger for classes and functions inside this
    module. When there is no global logging configured with according handlers,
    a default StreamHandler with sensible formatting will be defined.

    Parameters
    ----------
    name: str
        Name of the logging hierarchy to use. Caller is responsible of
        generating the correct name (i.e. package.submodule.classname). In a
        class, set this to f'{__name__}.{self.__class__.__name__}'.

    Returns
    -------
    logger: :class:logging.logger
        The according logger.
    """
    logger = logging.getLogger(name)
    if not logging.root.handlers and logger.level == logging.NOTSET:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)-8s - %(message)s "
            "[%(name)s/%(funcName)s | %(threadName)s (PID:%(process)d)]",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
