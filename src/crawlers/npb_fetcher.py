import requests
from bs4 import BeautifulSoup
from src.config import DEFEAULT_HEADERS, REQUEST_TIMEOUT, ENCODING


def fetch_playbyplay_contents(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=DEFEAULT_HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    response.encoding = ENCODING

    html = response.text
    soup = BeautifulSoup(html, "lxml")
    contents = soup.find("div", class_="contents")
    return contents


def extract_log_elements(contents: BeautifulSoup):
    return contents.select(".wrap tr, .wrap h5")
