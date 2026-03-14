class GameBoxState:
    def __init__(self, game_id: str, player_list: list, player_map: map):
        self.game_id = game_id
        self.inning = 1
        self.half = True
        self.away = None
        self.home = None

        self.player_list = player_list
        self.player_map = player_map

    def set_team_setting(self, team: str, batter_data: dict, pitcher_data: dict):
        team_data = {
            "score": 0,
            "SVO": False,
            "batting_order_index": 1,
            "fielding": {},
            "lineup": []
        }

        for batter in batter_data:
            player_id = self.player_map.get(batter["link"])
            batting_order = batter["batting_order"]
            positions = batter["positions"]
            if not batting_order:
                team_data["lineup"][batting_order] = player_id
                team_data["fielding"][positions[0]] = player_id

        for pitcher in pitcher_data:
            player_id = self.player_map.get(pitcher["link"])
            positions = pitcher["positions"]
            for pos in positions:
                if pos == "SP":
                    team_data["fielding"]["P"] = player_id

        if team == "away":
            self.away = team_data
        elif team == "home":
            self.home = team_data

    def check_svo(self, team: str, runner: int):
        if self.inning >= 7:
            if team == "home":
                lead = self.home["score"] - self.away["score"]
            else:
                lead = self.away["score"] - self.home["score"]
            
            if lead <= 3 and lead > 0:
                return True
            
            if (lead - runner) <= 2:
                return True
            
        return False

    def set_svo(self, team: str, svo: bool):
        if team == "away":
            self.away["SVO"] = svo
        elif team == "home":
            self.home["SVO"] = svo
    
    def inning_change(self):
        if self.half:
            self.half = False
        else:
            self.inning += 1
            self.half = True

    def update_score(self, runs: int):
        if self.half:
            self.away["score"] += runs
        else:
            self.home["score"] += runs

    def change_pitcher(self, pitcher_id: int, order: int | None):
        if self.half:
            self.home["fielding"]["P"] = pitcher_id
            if not order:
                self.home["lineup"][order] = pitcher_id
        else:
            self.away["fielding"]["P"] = pitcher_id
            if not order:
                self.away["lineup"][order] = pitcher_id
    
    def change_batter(self, batter_id: int):
        team = self.away if self.half else self.home
        order = team["batting_order_index"]
        team["lineup"][order] = batter_id

    def steal_event(self, log: dict):
        runner = log["batter_id"]
        pitcher = log["pitcher_id"]

        text = log["raw_TEXT"]

        if "盗塁成功" in text:
            return {"type": "SB", "runner": runner, "pitcher": pitcher, "catcher": 0, "fielder": 0, "base": 2, "double": False}
        
        if "盗塁失敗" in text:
            return {"type": "CS", "runner": runner, "pitcher": pitcher, "catcher": 0, "fielder": 0, "base": 2, "double": False}
        
        if "牽制アウト" in text:
            return {"type": "PK", "runner": runner, "pitcher": pitcher, "catcher": 0, "fielder": 0, "base": 2}
        
        return None

    def batting_event(self):
        return

    def pitching_event(self):
        return
    
    def fielding_event(self):
        return