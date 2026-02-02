class NPBResolver:
    def get_game_count(self, start_date, end_date):
        return

    def get_game_urls(self, start_date, end_date):
        return
    
    def playbyplay_url(self, game_url):
        return game_url + "/playbyplay.html"
    
    def box_url(self, game_url):
        return game_url + "/box.html"
    
    def roster_url(self, game_url):
        return game_url + "/roster.html"
    
    def game_info_url(self, game_url):
        return game_url