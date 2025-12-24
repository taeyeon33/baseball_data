import json
from src.repositories.admin_repositories import fetch_all_tables, fetch_all_players

def get_all_tables():
    schema = fetch_all_tables()
    rows = json.dumps(schema, indent=2, ensure_ascii=False)
    return rows

def get_all_players():
    rows = fetch_all_players()

    return rows
    return [
        {
            "player_id": row["player_id"],
            "name": row["name"],
            "team_id": row["team_id"]
        }
        for row in rows
    ]    