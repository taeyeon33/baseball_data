import requests
from bs4 import BeautifulSoup
from src.config import DEFEAULT_HEADERS, REQUEST_TIMEOUT, ENCODING

def fetch_html(url: str) -> BeautifulSoup:
    try:
        res = requests.get(url, headers=DEFEAULT_HEADERS, timeout=REQUEST_TIMEOUT)
        res.raise_for_status()
        res.encoding = ENCODING

        html = res.text
        return BeautifulSoup(html, "lxml")
    except Exception as e:
        return None