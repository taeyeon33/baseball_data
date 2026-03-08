import re
from bs4 import BeautifulSoup
import traceback

class NPBBoxParser:
    @staticmethod
    def parse_participation_data(html: BeautifulSoup, away_team_id: int, home_team_id: int):
        contents = html.select_one(".contents")
        if not contents:
            return None

        participation = []

        batter_tables = [
            (contents.select("#table_top_b > table > tbody > tr"), away_team_id),
            (contents.select("#table_bottom_b > table > tbody > tr"), home_team_id)
        ]

        for rows, team_id in batter_tables:
            now_order = None

            for row in rows:
                part = {
                    "team_id": team_id,
                    "player_name": None,
                    "link": None,
                    "positions": [],
                    "batting_order": None,
                    "is_starting": False,
                    "decisions": None
                }

                try:
                    tds = row.find_all("td")
                    if len(tds) < 3:
                        continue

                    order_text = tds[0].get_text(strip=True)

                    if order_text:
                        now_order = int(order_text)
                        part["batting_order"] = now_order
                        part["is_starting"] = True
                    else:
                        part["batting_order"] = now_order

                    pos_text = re.sub(r"^（.*?）", "", tds[1].get_text(strip=True))
                    for p in pos_text:
                        mapped = NPBBoxParser.position_mapping(p)
                        if mapped:
                            part["positions"].append(mapped)

                    name_tag = tds[2].select_one("a")
                    if name_tag:
                        part["player_name"] = name_tag.get_text(strip=True)
                        href = name_tag.get("href")
                        match = re.search(r"/(\d+)\.html$", href)
                        if match:
                            part["link"] = match.group(1)

                    participation.append(part)

                except Exception:
                    traceback.print_exc()
                    continue

        pitcher_tables = [
            (contents.select("#table_top_p > table > tbody > tr"), away_team_id),
            (contents.select("#table_bottom_p > table > tbody > tr"), home_team_id)
        ]

        for rows, team_id in pitcher_tables:
            last_index = len(rows) - 1

            for idx, row in enumerate(rows):
                part = {
                    "team_id": team_id,
                    "player_name": None,
                    "positions": [],
                    "batting_order": None,
                    "is_starting": False,
                    "decisions": None
                }

                try:
                    tds = row.find_all("td")
                    if len(tds) < 2:
                        continue

                    decisions = tds[0].get_text(strip=True)

                    if "H" in decisions:
                        part["decisions"] = "HD"
                    elif "○" in decisions:
                        part["decisions"] = "W"
                    elif "●" in decisions:
                        part["decisions"] = "L"
                    elif "S" in decisions:
                        part["decisions"] = "SV"

                    name_tag = tds[2].select_one("a")
                    if name_tag:
                        part["player_name"] = name_tag.get_text(strip=True)
                        href = name_tag.get("href")
                        match = re.search(r"/(\d+)\.html$", href)
                        if match:
                            part["link"] = match.group(1)

                    if idx == 0:
                        part["positions"].append("SP")
                        part["is_starting"] = True
                    elif idx == last_index:
                        part["positions"].append("CP")
                    else:
                        part["positions"].append("RP")

                    participation.append(part)

                except Exception:
                    traceback.print_exc()
                    continue

        return participation
    
    @staticmethod
    def parse_away_batter_data(html: BeautifulSoup):
        contents = html.select_one(".contents")
        if not contents:
            return None

        table = contents.select("#table_top_b > table > tbody > tr")

        away_batter_data = NPBBoxParser.batter_data(table)

        return away_batter_data
    
    @staticmethod
    def parse_home_batter_data(html: BeautifulSoup):
        contents = html.select_one(".contents")
        if not contents:
            return None
        
        table = contents.select("#table_bottom_b > table > tbody > tr")

        home_batter_data = NPBBoxParser.batter_data(table)

        return home_batter_data
    
    @staticmethod
    def parse_away_pitcher_data(html: BeautifulSoup):
        contents = html.select_one(".contents")
        if not contents:
            return None
        
        table = contents.select("#table_top_p > table > tbody > tr")

        away_pitcher_data = NPBBoxParser.pitcher_data(table)

        return away_pitcher_data
    
    @staticmethod
    def parse_home_pitcher_data(html: BeautifulSoup):
        contents = html.select_one(".contents")
        if not contents:
            return None
        
        table = contents.select("#table_bottom_p > table > tbody > tr")

        home_pitcher_data = NPBBoxParser.pitcher_data(table)

        return home_pitcher_data
    
    @staticmethod
    def batter_data(table: BeautifulSoup):
        batter_list = []

        now_order = None
        for row in table:
            cols = row.find_all("td")
            batter = {
                "batting_order": None,
                "positions": [],
                "player_name": None,
                "link": None,
                "AB": 0,
                "R": 0,
                "H": 0,
                "RBI": 0,
                "SB": 0,
                "at_bats": []
            }

            order_text = cols[0].get_text(strip=True)
            if order_text:
                now_order = int(order_text)
                batter["batting_order"] = now_order
            else:
                batter["batting_order"] = now_order

            pos_text = re.sub(r"^（.*?）", "", cols[1].get_text(strip=True))
            for p in pos_text:
                mapped = NPBBoxParser.position_mapping(p)
                if mapped:
                    batter["positions"].append(mapped)

            name_tag = cols[2].select_one("a")
            if name_tag:
                batter["player_name"] = name_tag.get_text(strip=True)
                href = name_tag.get("href")
                match = re.search(r"/(\d+)\.html$", href)
                if match:
                    batter["link"] = match.group(1)

            batter["AB"] = NPBBoxParser._safe_int(cols[3].get_text(strip=True))
            batter["R"] = NPBBoxParser._safe_int(cols[4].get_text(strip=True))
            batter["H"] = NPBBoxParser._safe_int(cols[5].get_text(strip=True))
            batter["RBI"] = NPBBoxParser._safe_int(cols[6].get_text(strip=True))
            batter["SB"] = NPBBoxParser._safe_int(cols[7].get_text(strip=True))

            for col in cols[8:]:
                batter["at_bats"].append(col.get_text(strip=True))
        
            batter_list.append(batter)

        return batter_list

    @staticmethod
    def pitcher_data(table: BeautifulSoup):
        pitcher_list = []

        last_index = len(table) - 1

        for idx, row in enumerate(table):
            cols = row.find_all("td")
            pitcher = {
                "positions": [],
                "decisions": None,
                "player_name": None,
                "link": None,
                "NP": 0,
                "AB": 0,
                "IP_outs": 0,
                "H": 0,
                "HR": 0,
                "BB": 0,
                "HBP": 0,
                "SO": 0,
                "WP": 0,
                "BK": 0,
                "R": 0,
                "ER": 0
            }

            if idx == 0:
                pitcher["positions"].append("SP")
            elif idx == last_index:
                pitcher["positions"].append("CP")
            else:
                pitcher["positions"].append("RP")

            decisions = cols[0].get_text(strip=True)
            if "H" in decisions:
                pitcher["decisions"] = "HD"
            elif "○" in decisions:
                pitcher["decisions"] = "W"
            elif "●" in decisions:
                pitcher["decisions"] = "L"
            elif "S" in decisions:
                pitcher["decisions"] = "SV"

            name_tag = cols[1].select_one("a")
            if name_tag:
                pitcher["player_name"] = name_tag.get_text(strip=True)
                href = name_tag.get("href")
                match = re.search(r"/(\d+)\.html$", href)
                if match:
                    pitcher["link"] = match.group(1)

            pitcher["NP"] = NPBBoxParser._safe_int(cols[2].get_text(strip=True))
            pitcher["AB"] = NPBBoxParser._safe_int(cols[3].get_text(strip=True))

            ip_th = cols[4].select_one("th")
            ip_td = cols[4].select_one("td")

            inning = NPBBoxParser._safe_int(ip_th.get_text(strip=True))
            extra = ip_td.get_text(strip=True) if ip_td else ""

            outs = 0
            if extra == ".1":
                outs = 1
            elif extra == ".2":
                outs = 2
            elif "+" in extra:
                outs = 0

            pitcher["IP_outs"] = inning * 3 + outs

            pitcher["H"] = NPBBoxParser._safe_int(cols[5].get_text(strip=True))
            pitcher["HR"] = NPBBoxParser._safe_int(cols[6].get_text(strip=True))
            pitcher["BB"] = NPBBoxParser._safe_int(cols[7].get_text(strip=True))
            pitcher["HBP"] = NPBBoxParser._safe_int(cols[8].get_text(strip=True))
            pitcher["SO"] = NPBBoxParser._safe_int(cols[9].get_text(strip=True))
            pitcher["WP"] = NPBBoxParser._safe_int(cols[10].get_text(strip=True))
            pitcher["BK"] = NPBBoxParser._safe_int(cols[11].get_text(strip=True))
            pitcher["R"] = NPBBoxParser._safe_int(cols[12].get_text(strip=True))
            pitcher["ER"] = NPBBoxParser._safe_int(cols[13].get_text(strip=True))

            pitcher_list.append(pitcher)

        return pitcher_list
    
    @staticmethod
    def position_mapping(position: str):
        positions = {
            "右": "RF",
            "中": "CF",
            "左": "LF",
            "遊": "SS",
            "三": "3B",
            "二": "2B",
            "一": "1B",
            "捕": "C",
            "投": "P",
            "指": "DH",
            "走": "PR",
            "打": "PH"
        }
        return positions.get(position)
    
    @staticmethod
    def _safe_int(text: str):
        return int(text) if text.isdigit() else 0