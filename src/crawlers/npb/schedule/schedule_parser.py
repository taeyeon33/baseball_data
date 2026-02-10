from bs4 import BeautifulSoup
from datetime import datetime

class NPBScheduleParser:
    def parse_url(html: BeautifulSoup, cur: datetime):
        url_list = list()

        if not html:
            return url_list
        contents = html.select_one(".contents")

        month = cur.month
        day = cur.day

        tags = contents.select(f'tr[id="date{month:02}{day:02}"] a')

        if not tags:
            return url_list

        for t in tags:
            href = t.get("href")
            if href:
                url_list.append(f"https://npb.jp{href}")

        return url_list