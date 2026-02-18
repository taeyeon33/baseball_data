from datetime import datetime, timedelta
from src.crawlers.common.html_fetcher import fetch_html
from src.crawlers.npb.schedule.schedule_parser import NPBScheduleParser

def get_game_urls(schedule_urls: list, start_date: datetime, end_date: datetime):
    game_urls = list()
    
    try:
        cur = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        for s_url in schedule_urls:
            html = fetch_html(s_url)
            while  cur <= end:
                g_urls = NPBScheduleParser.parse_url(html, cur)
                for g_url in g_urls:
                    game_urls.append(g_url)
                cur += timedelta(days=1)
        
        return game_urls
        
    except Exception as e:
        return game_urls