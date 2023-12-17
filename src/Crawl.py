class Crawl:

    def __init__(self, id: str, url: str) -> None:
        self._id: str = id
        self._url: str = url

    @property
    def id(self) -> str:
        return self._id

    @property
    def url(self) -> str:
        return self._url
