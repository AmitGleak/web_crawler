import time
import requests
from multiprocessing import Queue
from app_config import CrawlStatus
import src.datastore as datastore
from src.controllers.BaseController import BaseController
from src.Crawl import Crawl


class CrawlProcessController(BaseController):

    def __init__(self, queue: Queue, controller_name: str) -> None:
        super().__init__(queue, controller_name)

    def _process_crawl(self, crawl: Crawl) -> None:
        try:
            datastore.set_crawl_status(crawl.id, CrawlStatus.RUNNING)
            response: requests.Response = requests.get(crawl.url)

            if response.status_code != 200:
                self.logger.log.error(f'Crawl failed. Crawl ID: {crawl.id}, URL: {crawl.url}, '
                                      f'status code: {response.status_code}')
                datastore.set_crawl_status(crawl.id, CrawlStatus.ERROR)
            else:
                datastore.save_html(crawl.id, response.text)
                datastore.set_crawl_status(crawl.id, CrawlStatus.COMPLETE)
                self.logger.log.info(f'Crawl completed successfully. Crawl ID: {crawl.id}, URL: {crawl.url}')
        except requests.exceptions.ConnectionError as e:
            datastore.set_crawl_status(crawl.id, CrawlStatus.ERROR)
            self.logger.log.error(f'Encountered error in crawl request. Error: {e}')

    def run(self) -> None:
        self.initialize_logger()
        self.logger.log.info(f'{self.controller_name} running')
        while True:
            try:
                if self.queue.qsize() > 0:
                    crawl: Crawl = self.queue.get(block=True, timeout=5)
                    self._process_crawl(crawl)
            except Exception as e:
                self.logger.log.info(f'Encountered error while processing crawl. Error: {e}')
                time.sleep(5)
