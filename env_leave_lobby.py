
from pony.orm import db_session, commit
#debo importar el player
from db.database import Player as db_player
from db.database import Match as db_match
from db.database import Lobby as db_lobby
from definitions import match_status
from pony import *

with db_session:
    the_player1 = db_player(player_name= "Leo Messi", player_ingame = False, player_isHost=True,
                            player_dead = False, player_position = 0, player_exchangeR = 0, player_exchangeL = 0,
                            player_role = 0, player_lobby = None, player_current_match_id = None, player_status = 0, player_quarentine_count = 0)

    the_player2 = db_player(player_name= "Messi", player_ingame = False, player_isHost=False,
                            player_dead = False, player_position = 0, player_exchangeR = 0, player_exchangeL = 0,
                            player_role = 0, player_lobby = None, player_current_match_id = None, player_status = 0, player_quarentine_count = 0)

    commit()

    the_match =db_match(match_status = match_status.INITIALIZED.value, match_direction = True,
                        match_currentP = the_player2.player_id, match_cardsCount = 0)

    commit()

    the_lobby = db_lobby(lobby_name = "la seleccion", lobby_max = 6, lobby_min = 5,
                         lobby_password = None, lobby_pcount = 6, lobby_match = the_match.match_id)

    commit()

    the_player1.player_lobby = the_lobby.lobby_id
    the_player1.player_current_match_id = the_match.match_id

    the_player2.player_lobby = the_lobby.lobby_id
    the_player2.player_current_match_id = the_match.match_id

    commit()
