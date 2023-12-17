# Web Crawler

Web crawler implementation for the At-Bay home assignment.

## Installation

The application was developed using __**Python 3.12**__. Install the dependencies by running:

```bash
pip install -r requirements.txt
```

Please note that the application was developed on a Windows environment, files paths might need to be changed in __**app_config.py**__

## Usage
The application main file is __**src/WebCrawler.py**__. Running it will start all of the application components.

For the "/ingest" route, please pass the URL in the requests body with the key "url".

for the "/status" route, please pass the crawl ID as a URL parameter as - "/status?crawl_id=<CRAWL_ID>"
