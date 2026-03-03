class GameBoxState:
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.inning = 1
        self.half = True
        self.away = None
        self.home = None
        self.offence = None
        self.defense = None

    def set_team_setting(self, team: str, batter_data: dict, pitcher_data: dict):
        team_data = {
            "SVO": False,
            "batting_order_index": 1
        }

        for batter in batter_data:
            player_name = batter["player_name"]
            batting_order = batter["batting_order"]
            positions = batter["fielding"]
            if not batting_order:
                team_data["lineup"][batting_order] = player_name
                team_data["fielding"][positions[0]] = player_name

        for pitcher in pitcher_data:
            positions = pitcher["fielding"]
            for pos in positions:
                if pos == "SP":
                    team_data["fielding"]["P"] = pitcher["player_name"]

        if team == "away":
            self.away = team_data
            self.offence = team_data
        elif team == "home":
            self.home = team_data
            self.defense = team_data

    
    def set_svo(self, team: str, svo: bool):
        if team == "away":
            self.away["SVO"] = svo
        elif team == "home":
            self.home["SVO"] = svo
    
    def inning_change(self, change: dict):
        self.offence = self.defense
        self.defense = change
        if self.half:
            self.half = False
        else:
            self.half = True