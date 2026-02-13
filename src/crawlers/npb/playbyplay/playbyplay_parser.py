from bs4 import BeautifulSoup

class NPBPlaybyplayParser:
    @staticmethod
    def parse_pbp(html: BeautifulSoup):
        contents = html.select_one(".contents")
        if not contents:
            return None
        
        log_data = contents.select("#progress tbody tr, #progress h5")

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