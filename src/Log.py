import logging
from colorlog import ColoredFormatter


class Log:
    def __init__(self, name: str) -> None:
        self._log: logging = logging.getLogger(name)
        self._log.setLevel(logging.DEBUG)
        self._formatter = ColoredFormatter('%(log_color)s%(asctime)s - %(name)s - '
                                           '%(levelname)s%(reset)s %(light_white)s - %(message)s',
                                           datefmt=None,
                                           reset=True,
                                           log_colors={
                                               'DEBUG': 'cyan',
                                               'INFO': 'green',
                                               'WARNING': 'yellow',
                                               'ERROR': 'red',
                                               'CRITICAL': 'red,bg_white',
                                           },
                                           secondary_log_colors={},
                                           style='%')
        self._handler = logging.StreamHandler()
        self._handler.setFormatter(self._formatter)
        self._log.addHandler(self._handler)

    @property
    def log(self) -> logging:
        return self._log
