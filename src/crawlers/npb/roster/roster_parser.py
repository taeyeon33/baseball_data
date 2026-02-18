import re
from bs4 import BeautifulSoup

class NPBRosterParser:
    def parse_roster(html: BeautifulSoup, away_team_id: int, home_team_id: int):
        contents = html.select_one(".contents")
        if not contents:
            return None
        
        roster = []

        away_roster = contents.select(".half_left tr")
        home_roster = contents.select(".half_right tr")

        roster.extend(NPBRosterParser._extract_players(away_roster, away_team_id))
        roster.extend(NPBRosterParser._extract_players(home_roster, home_team_id))
        
        return roster
    
    def _extract_players(rows, team_id):
        players = []

        for row in rows:
            th = row.select_one("th")
            if not th:
                num_dom = row.select_one(".num")
                number = num_dom.get_text(strip=True) if num_dom else None
                name_tag = row.select_one("a")
                href = name_tag.get("href") if name_tag else None
                match = re.search(r"/(\d+)\.html$", href)
                if match:
                    link_number = match.group(1)
                name = name_tag.get_text(strip=True) if name_tag else None

                players.append({
                    "number": number,
                    "link": link_number,
                    "name": name,
                    "team_id": team_id,
                })

        return players