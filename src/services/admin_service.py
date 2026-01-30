import json
from src.repositories.admin_repositories import fetch_all_tables, fetch_data_list, table_exists, get_columns, insert_row, get_data, update_row, delete_row

def get_all_tables():
    schema = fetch_all_tables()
    rows = json.dumps(schema, indent=2, ensure_ascii=False)
    return rows

def get_data_list(data):
    table = data["table"]
    if not table:
        raise ValueError("테이블이 존재하지 않습니다.")
    
    if not table_exists("one", table):
        raise ValueError("테이블이 존재하지 않습니다.")
    
    options = None
    if "player_team_history" in table or "player_positions" in table:
        options = {"player_name": True}
    if (table == "positions"):
        options = {"positions": True}
    
    rows = fetch_data_list(table, options=options)

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
        raise ValueError("테이블이 존재하지 않습니다.")
    
    if not table_exists("one", table):
        raise ValueError("테이블이 존재하지 않습니다.")
    
    columns = get_columns(table)
    valid_columns = {col["name"] for col in columns}

    rows = {
        k: v
        for k, v in data.items()
        if k in valid_columns
    }

    if not rows:
        raise ValueError("컬럼이 존재하지 않습니다.")

    result = insert_row(table, rows)
    return result

def update_data(data):
    table = data["table"]
    if not table:
        raise ValueError("테이블이 존재하지 않습니다.")
    
    if not table_exists("one", table):
        raise ValueError("테이블이 존재하지 않습니다.")

    rows = {
        k: v
        for k, v in data.items()
        if "id" in k or "code" in k
    }

    select_data = get_data(table, rows)
    if select_data is None:
        raise ValueError("수정할 데이터가 존재하지 않습니다.")
    
    updateCol = {
        k: v
        for k, v in data.items()
        if "id" not in k or "code" not in k
    }
    del updateCol["table"]

    result = update_row(table, updateCol, rows)
    return result

def delete_data(data):
    table = data["table"]
    if not table:
        raise ValueError("테이블이 존재하지 않습니다.")
    
    if not table_exists("one", table):
        raise ValueError("테이블이 존재하지 않습니다.")

    rows = {
        k: v
        for k, v in data.items()
        if "id" in k or "code" in k
    }

    select_data = get_data(table, rows)
    if select_data is None:
        raise ValueError("삭제할 데이터가 존재하지 않습니다.")
    
    result = delete_row(table, rows)
    return result