import requests
from bs4 import BeautifulSoup
from src.config import DEFEAULT_HEADERS, REQUEST_TIMEOUT, ENCODING

from src.crawlers.common.base_fetcher import BaseFetcher

class NPBPlayByPlayFetcher(BaseFetcher):
    def fetch(self, url):
        res = requests.get(url, headers=DEFEAULT_HEADERS, timeout=REQUEST_TIMEOUT)
        res.raise_for_status()
        res.encoding = ENCODING

        html = res.text
        soup = BeautifulSoup(html, "lxml")
        contents = soup.find("div", class_="contents")
        return contents