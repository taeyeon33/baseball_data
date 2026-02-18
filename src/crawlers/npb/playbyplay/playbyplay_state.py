class GameLogState:
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.inning = 1
        self.half = True
        self.seq = 0
        self.out = None
        self.on_1b = False
        self.on_2b = False
        self.on_3b = False
        self.ball = 0
        self.strike = 0
        self.batter_id = None
        self.away_pitcher_id = None
        self.home_pitcher_id = None
        self.detail_code = None

    def parse_inning(self, text: str):
        self.seq = 0
        parts = text.split()
        inning_text = parts[0].split("回")
        self.inning = int(inning_text[0])
        self.half = True if "表" in inning_text[1] else False

    def apply(self, event: dict):
        if event["type"] == "inning_change":
            self._inning_change(event)
        elif event["type"] == "play":
            self._update_play_state(event)
        elif event["type"] == "pitching_change":
            self._change_pitcher(event)
        elif event["type"] == "pinch_hitter":
            self._change_batter(event)
        elif event["type"] == "steal_base":
            self._update_steal_base(event)
        
        return self._to_log_row(event)
    
    def _inning_change(self, event: dict):
        if self.half:
            self.half = False
        if not self.half:
            self.inning += 1
            self.half = True
        self.seq = 0
        self.out = None
        self.on_1b = False
        self.on_2b = False
        self.on_3b = False
        self.ball = 0
        self.strike = 0
        self.batter_id = None
        self.detail_code = None
        self.parse_inning(event["raw_text"])
    
    def _change_pitcher(self, event: dict):
        pitcher_id = event["player_id"]
        if self.half:
            self.away_pitcher_id = pitcher_id
        else:
            self.home_pitcher_id = pitcher_id
    
    def _change_batter(self, event: dict):
        self.ball = 0
        self.strike = 0
        self.detail_code = None
        self.batter_id = event["player_id"]
    
    def _update_play_state(self, event: dict):
        log_arr = event["raw_text"].split()
        self.seq += 1
        self.out = int(log_arr[0].replace("アウト", ""))
        on_base = log_arr[1]
        self.on_1b = True if ("塁" in on_base and "1" in on_base) or "満塁" in on_base else False
        self.on_2b = True if ("塁" in on_base and "2" in on_base) or "満塁" in on_base else False
        self.on_3b = True if ("塁" in on_base and "3" in on_base) or "満塁" in on_base else False
        self.ball = int(log_arr[-2].replace("より", "").split("-")[0])
        self.strike = int(log_arr[-2].replace("より", "").split("-")[1])
        self.batter_id = event["player_id"]
        self.detail_code = event["detail_code"]

    def _update_steal_base(self, event: dict):
        log_arr = event["raw_text"].split()
        self.out = int(log_arr[0].replace("アウト", ""))
        on_base = log_arr[1]
        self.on_1b = True if ("塁" in on_base and "1" in on_base) or "満塁" in on_base else False
        self.on_2b = True if ("塁" in on_base and "2" in on_base) or "満塁" in on_base else False
        self.on_3b = True if ("塁" in on_base and "3" in on_base) or "満塁" in on_base else False
        self.ball = 0
        self.strike = 0
        self.batter_id = event["player_id"]
        self.detail_code = event["detail_code"]

    def _to_log_row(self, event: dict):
        return {
            "game_id": self.game_id,
            "season_id": event["season_id"],
            "inning": self.inning,
            "half": "top" if self.half else "bottom",
            "seq": self.seq,
            "log_type": event["type"],
            "batter_id": self.batter_id,
            "pitcher_id": self.away_pitcher_id if self.half else self.home_pitcher_id,
            "ball": self.ball,
            "strike": self.strike,
            "out": self.out,
            "on_1b": self.on_1b,
            "on_2b": self.on_2b,
            "on_3b": self.on_3b,
            "detail_code": self.detail_code,
            "raw_text": event["raw_text"],
        }