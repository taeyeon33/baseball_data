import re
from bs4 import BeautifulSoup

from googletrans import Translator


class PlayerParser:
    @staticmethod
    def get_player(html: BeautifulSoup):
        contents = html.select_one(".contents")
        player = dict()

        name_tag = contents.select_one("li#pc_v_name")
        kana_tag = contents.select_one("li#pc_v_kana")

        name_text = ""

        if kana_tag and re.search(r"\([A-Za-z\s\.]+\)", kana_tag.get_text()):
            kana_raw = kana_tag.get_text(strip=True).replace("\u3000", " ").replace("・", " ")
            name_text = re.sub(r"\(.*?\)", "", kana_raw).strip()
        
        elif name_tag:
            small = name_tag.select_one("small")

            if small:
                name_text = small.get_text(strip=True).strip("（）() ").replace("\u3000", " ")
            else:
                raw_text = name_tag.get_text(" ", strip=True).replace("\u3000", " ")
                name_text = raw_text

        name_text = name_text.strip()
        parts = name_text.split()

        if len(parts) == 2:
            if name_tag.find("small"):
                player["first_name"], player["last_name"] = parts
            else:
                player["last_name"], player["first_name"] = parts
        else:
            player["last_name"] = name_text
            player["first_name"] = ""

        for row in contents.select("#pc_bio tr"):
            th = row.th.text.strip()
            td = row.td.text.strip()

            if th == "投打":
                p_raw = td.split("投")[0]
                b_raw = td.split("打")[0][-1]

                hand_map = {
                    "右": "우",
                    "左": "좌",
                    "両": "양"
                }

                player["pitching"] = hand_map.get(p_raw, p_raw)
                player["batting"] = hand_map.get(b_raw, b_raw)

            elif th == "身長／体重":
                m = re.search(r"(\d+)cm／(\d+)kg", td)
                if m:
                    player["height"] = int(m.group(1))
                    player["weight"] = int(m.group(2))

            elif th == "生年月日":
                m = re.search(r"(\d+)年(\d+)月(\d+)日", td)
                if m:
                    y, mth, d = m.groups()
                    player["birthday"] = f"{y}-{mth.zfill(2)}-{d.zfill(2)}"

            elif th == "経歴":
                player["school"] = td

            elif th == "ドラフト":
                if not td:
                    player["country"] = "외국"
                    player["first_name"], player["last_name"] = \
                        player["last_name"], player["first_name"]
                else:
                    player["country"] = "일본"
                player["draft"] = td

        photo_tag = contents.select_one("#pc_v_photo img")
        if photo_tag:
            player["photo"] = photo_tag.get("src")
        print(player)
        return player

    @staticmethod
    def get_player_name(html: BeautifulSoup, eng_html: BeautifulSoup, player_id: str):
        contents = html.select_one(".contents")
        eng_contents = eng_html.select_one(".contents") if eng_html else None

        player_name = {"player_id": player_id}

        kana_tag = contents.select_one("li#pc_v_kana")

        jp_last = ""
        jp_first = ""

        if kana_tag:
            kana_text = kana_tag.get_text(strip=True)

            is_foreign = bool(re.search(r"\([A-Z\s]+\)", kana_text))

            bracket_match = re.search(r"（([^）]+)）", kana_text)
            if bracket_match:
                full_name = bracket_match.group(1).strip()
            else:
                full_name = kana_text.strip()

            if "・" in full_name:
                jp_last, jp_first = [x.strip() for x in full_name.split("・", 1)]
            else:
                parts = full_name.split()
                jp_last = parts[0]
                jp_first = parts[1] if len(parts) > 1 else ""

        player_name["jp_last_name"] = jp_last.strip()
        player_name["jp_first_name"] = jp_first.strip()

        if is_foreign:
            player_name["jp_first_name"], player_name["jp_last_name"] = \
                player_name["jp_last_name"], player_name["jp_first_name"]

            player_name["jp_last_name"] = player_name["jp_last_name"].split("\u3000")[0]

            if not eng_contents:
                en_match = re.search(r"\(([A-Za-z\s]+)\)", kana_tag.get_text(strip=True))
                if en_match:
                    en_full = en_match.group(1).strip().title()
                    parts = en_full.split()

                    if len(parts) >= 2:
                        player_name["en_first_name"] = parts[0]
                        player_name["en_last_name"] = " ".join(parts[1:])
                    elif len(parts) == 1:
                        player_name["en_last_name"] = parts[0]
        else:
            if bracket_match:
                player_name["jp_first_name"], player_name["jp_last_name"] = \
                    player_name["jp_last_name"], player_name["jp_first_name"]
            eng_name_li = eng_contents.select_one("li#pc_v_name") if eng_contents else None
            if eng_name_li:
                eng_name = eng_name_li.text.strip()
                if "," in eng_name:
                    last, first = [x.strip() for x in eng_name.split(",", 1)]
                    player_name["en_last_name"] = last
                    player_name["en_first_name"] = first

        translator = Translator()
        
        player_name["ko_last_name"] = translator.translate(player_name["jp_last_name"], dest="ko").text
        player_name["ko_first_name"] = translator.translate(player_name["jp_first_name"], dest="ko").text
        print(player_name)
        return player_name

    @staticmethod
    def get_player_history(html: BeautifulSoup):
        contents = html.select_one(".contents")

        player_history = dict()

        stat_list = contents.select(".registerStats")
        for row in stat_list:
            year = row.select_one(".year").text.strip()
            team_name = row.select_one(".team").text.strip().replace("\u3000", " ").replace(" ", "")

            if year not in player_history:
                player_history[year] = []

            player_history[year].append(team_name)

        return player_history