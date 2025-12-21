def insert_game_log(cur, row, log_type):
    if (log_type != "play"):
        row["seq"] = 0
        row["ball"] = 0
        row["strike"] = 0
    if (log_type == "pitching_change"):
        row["batter_id"] = None
    if (log_type == "pinch_hitter"):
        row["pitcher_id"] = None
    if (log_type == "inning_change"):
        row["pitcher_id"] = None
        row["batter_id"] = None

    cur.execute(
        """
        INSERT INTO game_logs (
            game_id, inning, half, seq, log_type,
            out, on_1b, on_2b, on_3b, ball, strike,
            batter_id, pitcher_id, detail_code, raw_text
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row["game_id"],
            row["inning"],
            row["half"],
            row.get("seq", 0),
            row["log_type"],
            row.get("out", None),
            row.get("on_1b", False),
            row.get("on_2b", False),
            row.get("on_3b", False),
            row.get("ball", 0),
            row.get("strike", 0),
            row.get("batter_id", None),
            row.get("pitcher_id", None),
            row.get("detail_code", None),
            row.get("raw_text"),
        ),
    )