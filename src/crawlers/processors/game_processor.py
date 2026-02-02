def process_game(game_url, resolver):
    game_info = resolver.resolve_game_info(game_url)
    game_id = insert_game(game_info)