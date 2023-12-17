class AppConfig:
    APP_ROOT_DIR = 'C:\\web_crawler\\'
    DB_NAME = 'crawls.db'
    CRAWLS_TABLE_NAME = 'crawls'
    HTML_DIR_NAME = 'html\\'
    HTML_DIR = f'{APP_ROOT_DIR}{HTML_DIR_NAME}'
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 5000
    SERVER_APP_NAME = 'Web Crawler API'


class CrawlStatus:
    ACCEPTED = 'Accepted'
    RUNNING = 'Running'
    ERROR = 'Error'
    COMPLETE = 'Complete'
    NOT_FOUND = 'Not-Found'
