import json
from src.repositories.admin_repositories import fetch_all_tables, fetch_all_players, table_exists, get_columns, insert_row

def get_all_tables():
    schema = fetch_all_tables()
    rows = json.dumps(schema, indent=2, ensure_ascii=False)
    return rows

def get_all_players():
    rows = fetch_all_players()

    return [dict(row) for row in rows]
    return [
        {
            "player_id": row["player_id"],
            "name": row["name"],
            "team_id": row["team_id"]
        }
        for row in rows
    ]

def insert_data(data):
    table = data["table"]
    if not table:
        return "테이블이 존재하지 않습니다."
    
    if not table_exists("one", table):
        return "테이블이 존재하지 않습니다."
    
    columns = get_columns(table)
    valid_columns = {col["name"] for col in columns}

    rows = {
        k: v
        for k, v in data.items()
        if k in valid_columns
    }
    print(rows)

    if not rows:
        return "컬럼이 존재하지 않습니다."

    result = insert_row(table, rows)
    return result