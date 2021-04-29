import logging
import inspect


class MetaBase(type):
    """Creates a singleton derived classes"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaBase, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Base(metaclass=MetaBase):
    _logger = None

    @property
    def logger(self):
        if self._logger is None:
            # formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
            # logging.basicConfig(level=logging.WARN, format="%(asctime)s :%(levelname)s : %(name)s :%(message)s")
            logger_name = inspect.stack()[1][3]
            self._logger = logging.getLogger(logger_name)
            self._logger.setLevel(level=logging.DEBUG)
        return self._logger
