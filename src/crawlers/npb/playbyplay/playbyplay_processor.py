from src.crawlers.common.html_fetcher import fetch_html
from src.crawlers.npb.playbyplay.playbyplay_parser import NPBPlaybyplayParser
from src.crawlers.npb.playbyplay.playbyplay_state import GameLogState
from src.domain.results import GameProcessResult
from src.domain.enums import ProcessResult

def process_pbplog(game_url, game_id):
    try:
        html = fetch_html(game_url)
        if not html:
            return GameProcessResult(ProcessResult.FAILED, None)
        
        log_data = NPBPlaybyplayParser.parse_pbp(html)
        if not log_data:
            return GameProcessResult(ProcessResult.FAILED, None)
        
        state = GameLogState(game_id=1)

        log_count = 0
        for log in log_data:
            log_count += 1
            
            event = NPBPlaybyplayParser._get_log_type(log)
            if event["type"] == "pinch_hitter":
                row = state.apply(event)
                log_idx = insert_game_log(row, event["type"])
                if not log_idx:
                    return GameProcessResult(ProcessResult.FAILED, None)
                event["type"] = "play"
            row = state.apply(event)
            log_idx = insert_game_log(row, event["type"])

            
        
    except Exception as e:
        return e