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
                    for p in list(pos_text):
                        mapped = NPBBoxParser.position_mapping(p)
                        if mapped:
                            part["positions"].append(mapped)

                    name_tag = tds[2].select_one("a")
                    if name_tag:
                        part["player_name"] = name_tag.get_text(strip=True)

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
            print("총 투수 수:", len(rows))
            for idx, row in enumerate(rows):
                print(idx, ": ", row)
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

                    name_tag = tds[1].select_one("a")
                    if name_tag:
                        part["player_name"] = name_tag.get_text(strip=True)

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
        return
    
    @staticmethod
    def parse_home_batter_data(html: BeautifulSoup):
        return
    
    @staticmethod
    def parse_away_pitcher_data(html: BeautifulSoup):
        return
    
    @staticmethod
    def parse_home_pitcher_data(html: BeautifulSoup):
        return
    
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