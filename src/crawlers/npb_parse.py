def parse_log_element(log):
    text = log.get_text(separator=" ", strip=True)

    if log.name == "h5":
        return {"type": "inning_change", "raw_text": text}

    if "投手" in text:
        return {"type": "pitching_change", "raw_text": text}

    if "代打" in text:
        return {"type": "pinch_hitter", "raw_text": text}

    return {"type": "play", "raw_text": text}
