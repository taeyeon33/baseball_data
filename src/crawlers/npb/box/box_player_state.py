class PlayerBoxState:
    def __init__(self, game_id: str, away_team_id: int, home_team_id: int, player_map: map):
        self.game_id = game_id
        self.away_team_id = away_team_id
        self.home_team_id = home_team_id
        self.player_map = player_map
    
    @staticmethod
    def build_all_batter_data(self, away_batter_data: list, home_batter_data: list):
        all_batter_data = {}

        combined = [
            (away_batter_data, self.away_team_id),
            (home_batter_data, self.home_team_id)
        ]

        for team_data, team_id in combined:
            for raw in team_data:
                player_link = raw.get("link")
                player_id = self.player_map.get(player_link)

                if not player_id:
                    continue

                at_bats = raw.get("at_bats", [])

                PA = sum(1 for AB in at_bats if AB and AB != "-")

                AB = raw.get("AB", 0)
                H = raw.get("H", 0)
                RBI = raw.get("RBI", 0)
                R = raw.get("R", 0)
                SB = raw.get("SB", 0)

                all_dash = all(ab_text == "-" for ab_text in at_bats) if at_bats else True

                if all_dash and AB == 0 and H == 0 and RBI == 0 and R == 0 and SB == 0:
                    continue

                stat = {
                    "game_id": self.game_id,
                    "player_id": player_id,
                    "team_id": team_id,
                    "PA": PA,
                    "AB": AB,
                    "H": H,
                    "2B": 0,
                    "3B": 0,
                    "HR": 0,
                    "RBI": RBI,
                    "R": R,
                    "SB": SB,
                    "CS": 0,
                    "BB": 0,
                    "HBP": 0,
                    "IBB": 0,
                    "SO": 0,
                    "GDP": 0,
                    "SH": 0,
                    "SF": 0,
                    "GO": 0,
                    "AO": 0,
                }

                all_batter_data[player_id] = stat

        return all_batter_data
    
    @staticmethod
    def create_empty_pitcher_stat(self, player_id, team_id):
        return {
            "game_id": self.game_id,
            "player_id": player_id,
            "team_id": team_id,
            "GS": 0,
            "GR": 0,
            "GF": 0,
            "SVO": 0,
            "IP_outs": 0,
            "H": 0,
            "R": 0,
            "ER": 0,
            "HR": 0,
            "HBP": 0,
            "BB": 0,
            "SO": 0,
            "TBF": 0,
            "AB": 0,
            "NP": 0,
            "IBB": 0,
            "WP": 0,
            "BK": 0,
            "GDP": 0,
            "GO": 0,
            "AO": 0,
            "SB": 0,
            "CS": 0,
            "PK": 0,
        }
    
    @staticmethod
    def build_all_pitcher_data(self, away_pitcher_data, home_pitcher_data):
        all_pitcher_data = {}

        combined = [
            (away_pitcher_data, self.away_team_id),
            (home_pitcher_data, self.home_team_id)
        ]

        for team_data, team_id in combined:
            for raw in team_data:
                player_link = raw.get("link")
                player_id = self.player_map.get(player_link)

                if not player_id:
                    continue

                stat = PlayerBoxState.create_empty_pitcher_stat(player_id, team_id)

                role = raw.get("positions", [])
                if "SP" in role:
                    stat["GS"] = 1
                elif "RP" in role:
                    stat["GR"] = 1
                elif "CP" in role:
                    stat["GF"] = 1

                stat["NP"] = raw.get("NP", 0)
                stat["AB"] = raw.get("AB", 0)
                stat["IP_outs"] = raw.get("IP_outs", 0)
                stat["H"] = raw.get("H", 0)
                stat["HR"] = raw.get("HR", 0)
                stat["BB"] = raw.get("BB", 0)
                stat["HBP"] = raw.get("HBP", 0)
                stat["SO"] = raw.get("SO", 0)
                stat["ER"] = raw.get("ER", 0)
                stat["WP"] = raw.get("WP", 0)
                stat["BK"] = raw.get("BK", 0)

                all_pitcher_data[player_id] = stat

        return all_pitcher_data
    
    @staticmethod
    def build_all_fielding_data(self, away_batter_data, home_batter_data, away_pitcher_data, home_pitcher_data):
        all_fielding_data = {}

        combined = [
            (away_batter_data, self.away_team_id),
            (home_batter_data, self.home_team_id),
            (away_pitcher_data, self.away_team_id),
            (home_pitcher_data, self.home_team_id)
        ]

        for team_data, team_id in combined:
            for raw in team_data:
                player_link = raw.get("link")
                player_id = self.player_map.get(player_link)

                if not player_id:
                    continue

                stat = PlayerBoxState.create_empty_fielding_stat(player_id, team_id)

                role = raw

        return all_fielding_data