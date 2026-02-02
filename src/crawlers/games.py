from src.crawlers.npb.resolver import NPBResolver
from src.crawlers.processors.game_processor import process_game

def crawl_games(league: str, start_date, end_date):
    if not league:
        league = "NPB"
    
    if league == "NPB":
        resolver = NPBResolver()
    else:
        raise ValueError(f"{league}는 존재하지 않습니다.")
    
    game_count = resolver.get_game_count(start_date, end_date)

    if game_count < 1:
        raise ValueError("해당 날짜에 진행된 게임이 없습니다.")
    
    game_urls = resolver.get_game_urls(start_date, end_date)
    for game_url in game_urls:
        process_game(game_url, resolver)