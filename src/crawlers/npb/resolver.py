from datetime import datetime

class NPBResolver:
    def get_schedule_urls(self, start_date, end_date):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date,  "%Y-%m-%d")
        year = start_date.year
        url_list = list()

        if start_date.month != end_date.month:
            for m in range(start_date.month, end_date.month +  1):
                url = f"https://npb.jp/games/{year}/schedule_{m:02}_detail.html"
                url_list.append(url)
        else:
            url_list.append(f"https://npb.jp/games/{year}/schedule_{start_date.month:02}_detail.html")

        return url_list
    
    def playbyplay_url(self, game_url):
        return game_url + "/playbyplay.html"
    
    def box_url(self, game_url):
        return game_url + "/box.html"
    
    def roster_url(self, game_url):
        return game_url + "/roster.html"
    
    def game_info_url(self, game_url):
        return game_url