from src.crawlers.common.html_fetcher import fetch_html

def process_pbplog(game_url, game_id):
    try:
        html = fetch_html(game_url)
        if not html:
            return None
        contents = html.select_one(".contents")
        
        
        log_data = NPBPlaybyplayParser.parse_pbp(contents)
        
    except Exception as e:
        return e