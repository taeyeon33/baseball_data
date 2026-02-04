from bs4 import BeautifulSoup
from datetime import datetime

class NPBScheduleParser:
    def parse_url(contents: BeautifulSoup, cur: datetime):
        url_list = list()

        month = cur.month
        day = cur.day

        tags = contents.select(f'tr[id="date{month:02}{day:02}"] a')

        for t in tags:
            url_list.append(f"https://npb.jp{t['href']}")

        return url_list