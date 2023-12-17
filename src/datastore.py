import os
from app_config import AppConfig, CrawlStatus
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy import create_engine, Column, String, Integer, DateTime

if not os.path.exists(AppConfig.APP_ROOT_DIR):
    os.makedirs(AppConfig.APP_ROOT_DIR)
if not os.path.exists(AppConfig.HTML_DIR):
    os.makedirs(AppConfig.HTML_DIR)

Base = declarative_base()
engine = create_engine(f'sqlite:///{AppConfig.APP_ROOT_DIR}{AppConfig.DB_NAME}')
session_factory: sessionmaker = sessionmaker(bind=engine)
Session: scoped_session = scoped_session(session_factory)


class CrawlSchema(Base):
    __tablename__ = AppConfig.CRAWLS_TABLE_NAME
    id = Column(Integer, primary_key=True)
    crawl_id = Column(String, unique=True)
    status = Column(String)
    url = Column(String)
    creation_time = Column(DateTime, default=datetime.now(timezone.utc))
    html_file_path = Column(String)


Base.metadata.create_all(bind=engine)


def create_crawl(url: str) -> str:
    crawl_id = str(hash(url + str(datetime.now(timezone.utc))))
    crawl = CrawlSchema(crawl_id=crawl_id, url=url, status=CrawlStatus.ACCEPTED)

    with Session() as session:
        session.add(crawl)
        session.commit()

    return crawl_id


def set_crawl_status(crawl_id: str, status: CrawlStatus) -> None:
    with Session() as session:
        crawl = session.query(CrawlSchema).filter_by(crawl_id=crawl_id).first()
        crawl.status = status
        session.commit()


def get_crawl_status(crawl_id: str) -> str:
    with Session() as session:
        crawl = session.query(CrawlSchema).filter_by(crawl_id=crawl_id).first()
        return CrawlStatus.NOT_FOUND if not crawl else str(crawl.status)


def save_html(crawl_id: str, html_content: str) -> None:
    html_file_path: str = f'{AppConfig.HTML_DIR}{crawl_id}.html'
    with Session() as session:
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        crawl: CrawlSchema | None = session.query(CrawlSchema).filter_by(crawl_id=crawl_id).first()
        crawl.html_file_path = html_file_path
        session.commit()
        set_crawl_status(crawl_id, CrawlStatus.COMPLETE)
