import re
from bs4 import BeautifulSoup

class NPBPlaybyplayParser:
    @staticmethod
    def parse_pbp(html: BeautifulSoup):
        contents = html.select_one(".contents")
        if not contents:
            return None
        
        log_data = contents.select("#progress tr, #progress h5")
        del log_data[0]

        return log_data
    
    @staticmethod
    def _get_log_type(log: BeautifulSoup) -> str:
        text = log.get_text(separator=" ", strip=True)

        if log.name == "h5":
            return {"type": "inning_change", "raw_text": text}

        if "投手" in text:
            return {"type": "pitching_change", "raw_text": text}

        if "代打" in text:
            return {"type": "pinch_hitter", "raw_text": text}
        
        if "走者" in text:
            return {"type": "steal_base", "raw_text": text}

        return {"type": "play", "raw_text": text}
    
    @staticmethod
    def _get_player(log: BeautifulSoup) -> dict:
        player = {"name": None, "link": None}

        name_dom = log.select_one("a:last-child")
        if name_dom:
            player["name"] = name_dom.get_text(strip=True)
            href = name_dom.get("href")
            match = re.search(r"/(\d+)\.html$", href)
            if match:
                player["link"] = match.group(1)

        return player
    
    @staticmethod
    def _get_detail(log: BeautifulSoup) -> str:
        detail = None

        det_dom = log.select_one(".w2")
        if det_dom:
            detail = det_dom.get_text(strip=True)
        
        return detail