from multiprocessing import Queue, Process
from src.controllers.BaseController import BaseController
from src.controllers.IngestController import IngestController
from src.controllers.CrawlProcessController import CrawlProcessController
from src.Log import Log


class WebCrawler:
    def __init__(self) -> None:
        self._tasks_queue: Queue = Queue()
        self._controllers: list[BaseController] = [IngestController(self._tasks_queue, 'IngestController'),
                                                   CrawlProcessController(self._tasks_queue, 'CrawlProcessController')]
        self._controllers_processes: list[Process] = []
        self._logger: Log = Log('WebCrawler')

    def start(self) -> None:
        self._logger.log.info('WebCrawler started')
        for controller in self._controllers:
            controller_process: Process = Process(target=controller.run)
            controller_process.start()

        for process in self._controllers_processes:
            process.join()


if __name__ == '__main__':
    web_crawler: WebCrawler = WebCrawler()
    web_crawler.start()
