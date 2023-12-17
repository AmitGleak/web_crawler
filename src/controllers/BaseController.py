from multiprocessing import Queue
from abc import ABC, abstractmethod
from src.Log import Log


class BaseController(ABC):

    def __init__(self, queue: Queue, controller_name: str) -> None:
        self._queue: Queue = queue
        self._controller_name: str = controller_name
        self._logger: Log | None = None

    @property
    def queue(self) -> Queue:
        return self._queue

    @property
    def controller_name(self) -> str:
        return self._controller_name

    def initialize_logger(self) -> None:
        self._logger = Log(self._controller_name)

    @property
    def logger(self) -> Log:
        return self._logger

    @abstractmethod
    def run(self) -> None:
        pass
