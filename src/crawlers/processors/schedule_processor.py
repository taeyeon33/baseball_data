from datetime import datetime, timedelta
from src.crawlers.npb.fetchers.schedule_fetcher import NPBScheduleFetcher
from src.crawlers.npb.parsers.schedule_parser import NPBScheduleParser

def get_game_urls(schedule_urls, start_date, end_date):
    game_urls = list()

    cur = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    for s_url in schedule_urls:
        contents = NPBScheduleFetcher.fetch_contents(s_url)
        while  cur <= end:
            g_urls = NPBScheduleParser.parse_url(contents, cur)
            for g_url in g_urls:
                game_urls.append(g_url)
            cur += timedelta(days=1)
    
    return game_urls