from flask import Flask, request, jsonify
import src.datastore as datastore
from src.controllers.BaseController import BaseController
from app_config import AppConfig
from src.Crawl import Crawl
from multiprocessing import Queue


class IngestController(BaseController):

    def __init__(self, queue: Queue, controller_name: str) -> None:
        super().__init__(queue, controller_name)
        self._app: Flask | None = None

    def _setup_endpoints(self):
        @self._app.route('/ingest/', methods=['PUT'])
        def ingest_crawl():
            self.logger.log.info('Ingestion request received')
            url: str = request.form.get('url')

            if not url:
                self.logger.log.warning('URL is missing')
                return 'URL is missing', 400

            crawl_id: str = datastore.create_crawl(url)
            self.queue.put(Crawl(id=crawl_id, url=url))
            self.logger.log.info(f'Request handled. URL: {url}, Crawl ID: {crawl_id}')

            return f'crawl ID - {crawl_id}', 201

        @self._app.route('/status/', methods=['GET'])
        def get_crawl_status():
            crawl_id: str = request.args.get('crawl_id')
            crawl_status: str = datastore.get_crawl_status(crawl_id)
            self.logger.log.info(f'Crawl status - Crawl ID: {crawl_id}, Status: {crawl_status}')

            return jsonify({'crawl_status': crawl_status})

    def run(self) -> None:
        self.initialize_logger()
        self._app = Flask(AppConfig.SERVER_APP_NAME)
        self._setup_endpoints()
        self.logger.log.info(f'{self.controller_name} running')
        self._app.run(host=AppConfig.SERVER_HOST, port=AppConfig.SERVER_PORT)
