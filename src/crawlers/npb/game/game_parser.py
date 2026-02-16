import re
from bs4 import BeautifulSoup
from datetime import datetime

class NPBGameParser:
    @staticmethod
    def parse_game(html: BeautifulSoup):
        contents = html.select_one(".contents")
        game_info = contents.select_one(".game_info")
        info_text = game_info.get_text(strip=True) if game_info else None
        if not info_text:
            return None
        
        game_data = NPBGameParser._get_game_info(contents, info_text)

        return game_data

    @staticmethod
    def _get_game_info(contents: BeautifulSoup, text: str) -> dict:
        result = dict()
        score_list = NPBGameParser._parse_score_total(contents, NPBGameParser._parse_status(text))

        result = {
            "season_id": NPBGameParser._parse_season(contents),
            "game_date": NPBGameParser._parse_game_date(contents),
            "start_time": NPBGameParser._parse_start_time(text),
            "end_time": NPBGameParser._parse_end_time(text),
            "game_time": NPBGameParser._parse_duration(text),
            "game_type": NPBGameParser._parse_game_type(contents),
            "attendance": NPBGameParser._parse_attendance(text),
            "away_team_id": NPBGameParser._parse_team_name(contents, "top"),
            "home_team_id": NPBGameParser._parse_team_name(contents, "bottom"),
            "sta_id": NPBGameParser._parse_stadium(contents),
            "status": NPBGameParser._parse_status(text),
            "a_r": score_list["a_r"],
            "a_h": score_list["a_h"],
            "a_e": score_list["a_e"],
            "a_b": score_list["a_b"],
            "h_r": score_list["h_r"],
            "h_h": score_list["h_h"],
            "h_e": score_list["h_e"],
            "h_b": score_list["h_b"],
        }

        return result
    
    @staticmethod
    def _parse_season(contents: BeautifulSoup) -> str:
        game_date = NPBGameParser._parse_game_date(contents)
        year = game_date.year if game_date else None
        return year

    @staticmethod
    def _parse_game_date(contents: BeautifulSoup) -> datetime:
        game_date = None
        date_dom = contents.select_one(".game_tit time")
        date = date_dom.get_text(strip=True) if date_dom else None
        date_search = re.search(r"(\d{4}年\d{1,2}月\d{1,2}日)", date)

        if date_search:
            game_date = datetime.strptime(date_search.group(1), "%Y年%m月%d日")

        return game_date
    
    @staticmethod
    def _parse_start_time(text: str) -> str:
        start_time = None
        start = re.search(r"開始\s*(\d{1,2}:\d{2})", text)

        if start:
            start_time = start.group(1)

        return start_time
    
    @staticmethod
    def _parse_end_time(text: str) -> str:
        end_time = None
        end = re.search(r"終了\s*(\d{1,2}:\d{2})", text)

        if end:
            end_time = end.group(1)
        
        return end_time
    
    @staticmethod
    def _parse_duration(text: str) -> str:
        game_time = None
        duration = re.search(r"試合時間\s*(\d+)時間(\d+)分", text)

        if duration:
            h, m = duration.groups()
            game_time = f"{h}:{m.zfill(2)}"
        
        return game_time
    
    @staticmethod
    def _parse_game_type(contents: BeautifulSoup) -> str:
        game_type = None

        dom = contents.select_one(".game_tit h3")
        text = dom.get_text(strip=True) if dom else None
        if not text:
            return game_type

        if "公式戦" in text:
            game_type = "regular"
        if "オープン戦" in text:
            game_type = "exhibition"
        if "交流戦" in text:
            game_type = "interleague"
        if "オールスターゲーム" in text:
            game_type = "allstar"
        if "ファーストステージ" in text:
            game_type = "postseason"
        if "ファイナルステージ" in text:
            game_type = "postseason"
        if "日本シリーズ" in text:
            game_type = "postseason"

        return game_type
     
    @staticmethod
    def _parse_attendance(text: str) -> str:
        attendance = 0
        att = re.search(r"入場者\s*([\d,]+)人", text)
        
        if att:
            attendance = int(att.group(1).replace(",", ""))

        return attendance
    
    @staticmethod
    def _parse_team_name(contents: BeautifulSoup, tb: str) -> str:
        team_name = ""
        name_span = contents.select_one(f".{tb}>th>span")

        full = name_span.select_one(".hide_sp")
        if full:
            team_name = full.get_text(strip=True)
        else:
            team_name = name_span.get_text(strip=True) if name_span else None

        return team_name
    
    @staticmethod
    def _parse_stadium(contents: BeautifulSoup) -> str:
        sta_dom = contents.select_one(".game_tit .place")
        stadium = sta_dom.get_text(strip=True) if sta_dom else None

        return stadium

    @staticmethod
    def _parse_status(text: str) -> str:
        status = "unknown"

        if "中止" in text:
            status = "canceled"
            if "雨天のため中止" in text:
                status = "canceled_rain"
            if "グラウンド不良のため中止" in text:
                status = "canceled_ground"

        if "ノーゲーム" in text:
            status = "nogame"
            if "雨天のためノーゲーム" in text:
                status = "nogame_rain"
        
        if "雨天のためコールドゲーム" in text:
            status = "calledgame_rain"

        if "試合終了" in text:
            status = "finished"
        
        return status
    
    @staticmethod
    def _parse_score_total(contents: BeautifulSoup, status: str) -> dict:
        total_list = dict()

        if "canceled" in status or "nogame" in status:
            return {
                "a_r": 0,
                "a_h": 0,
                "a_e": 0,
                "a_b": 0,
                "h_r": 0,
                "h_h": 0,
                "h_e": 0,
                "h_b": 0,
            }

        top_board = contents.select(".top .total-1, .top .total-2")
        bot_board = contents.select(".bottom .total-1, .bottom .total-2")

        total_list = {
            "a_r": int(top_board[0].get_text(strip=True)) if top_board else 0,
            "a_h": int(top_board[1].get_text(strip=True)) if top_board else 0,
            "a_e": int(top_board[2].get_text(strip=True)) if top_board else 0,
            "a_b": 0,
            "h_r": int(bot_board[0].get_text(strip=True)) if bot_board else 0,
            "h_h": int(bot_board[1].get_text(strip=True)) if bot_board else 0,
            "h_e": int(bot_board[2].get_text(strip=True)) if bot_board else 0,
            "h_b": 0,
        }

        return total_list
    
    @staticmethod
    def _parse_score_by_inning(html: BeautifulSoup) -> dict:
        contents = html.select_one(".contents")
        if not contents:
            return None
        
        score_data = dict()

        top_inning = contents.select(".line-score .top td:not([class])")
        bot_inning = contents.select(".line-score .bottom td:not([class])")
        if not top_inning or not bot_inning:
            return None
        
        for i in range(1, len(top_inning) + 1):
            top_text = top_inning[i-1].get_text(strip=True)
            bot_text = bot_inning[i-1].get_text(strip=True)

            top_match = re.match(r"\d+", top_text)
            top_score = int(top_match.group()) if top_match else 0

            bot_match = re.match(r"\d+", bot_text)
            bot_score = int(bot_match.group()) if bot_match else 0

            score_data[i] = {
                "top": top_score,
                "bottom": bot_score,
                "bottom_raw": bot_text,
            }

            if bot_text.lower() == "x":
                break
        
        return score_data