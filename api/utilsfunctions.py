from db.database import Player, Match,Lobby
from pony.orm import db_session, commit

@db_session
def get_next_player_id(player_id, match_id):
    fetch_lobby = Lobby[match_id]
    
    fetch_match = fetch_lobby.lobby_match

    player_counter = fetch_lobby.lobby_pcount
    match_direction = fetch_match.match_direction

    current_player_obj = Player[player_id]
    current_player_pos = current_player_obj.player_position

    if match_direction:
        next_player_pos = (current_player_pos + 1) % player_counter
        next_player_obj = Player.get(lambda next: next.player_position == next_player_pos and next.player_current_match_id.match_id  == match_id)
        while next_player_obj.player_dead == True:
            next_player_pos = (next_player_pos + 1) % player_counter
            next_player_obj = Player.get(lambda next: next.player_position == next_player_pos and next.player_current_match_id.match_id  == match_id)
        next_player_id = next_player_obj.player_id
    else:
        next_player_pos = (current_player_pos - 1) % player_counter
        next_player_obj = Player.get(lambda next: next.player_position == next_player_pos and next.player_current_match_id.match_id  == match_id)
        while next_player_obj.player_dead == True:
            next_player_pos = (next_player_pos - 1) % player_counter
            next_player_obj = Player.get(lambda next: next.player_position == next_player_pos and next.player_current_match_id.match_id  == match_id)
        next_player_id = next_player_obj.player_id

    return next_player_id

@db_session
def can_exchange(player_id, match_id):
    player = Player[player_id]
    match = Match[match_id]

    if match.match_direction: # ronda va hacia la derecha
        locked_door = not (player.player_exchangeL)
    else: # ronda va hacia la izquierda
        locked_door = not (player.player_exchangeR)

    return not locked_door