from pony.orm import db_session, commit
from db.database import Match as db_match
from db.database import Lobby as db_lobby
from db.database import Player as db_player
from definitions import match_status

#primero creamos los players, luego un match y un lobby y los incluimos adentro
with db_session:
        the_player1 =db_player(player_name= "Leo Messi", player_ingame = False, player_isHost=True, 
                           player_dead = False, player_position = 0, player_exchangeR = 0, player_exchangeL = 0,
                            player_role = 0, player_lobby = None, player_current_match_id = None )
        the_player2 =db_player(player_name= "Dibu Martinez", player_ingame = False, player_isHost=False, 
                           player_dead = False, player_position = 1, player_exchangeR = 0, player_exchangeL = 0,
                            player_role = 0, player_lobby = None, player_current_match_id = None )
        the_player3 =db_player(player_name= "Julian alvarez", player_ingame = False, player_isHost=False, 
                           player_dead = True, player_position = 2, player_exchangeR = 0, player_exchangeL = 0,
                            player_role = 0, player_lobby = None, player_current_match_id = None )
        the_player4 =db_player(player_name="Angel Di Maria", player_ingame = False, player_isHost=False, 
                           player_dead = True, player_position = 3, player_exchangeR = 0, player_exchangeL = 0,
                            player_role = 0, player_lobby = None, player_current_match_id = None )
        the_player5 =db_player(player_name= "Alexis Mac Allister", player_ingame = False, player_isHost=False, 
                           player_dead = False, player_position = 4, player_exchangeR = 0, player_exchangeL = 0,
                            player_role = 0, player_lobby = None, player_current_match_id = None )
        the_player6 =db_player(player_name= "Nicolas Otamendi", player_ingame = False, player_isHost=False, 
                           player_dead = False, player_position = 5, player_exchangeR = 0, player_exchangeL = 0,
                            player_role = 0, player_lobby = None, player_current_match_id = None )
        commit()
        the_match =db_match(match_status = match_status.INITIALIZED.value, match_direction = True,
                                match_currentP = the_player2.player_id, match_cardsCount = 0)
        the_lobby = db_lobby(lobby_name = "la seleccion", lobby_max = 6, lobby_min = 5,
                                lobby_password = None, lobby_pcount = 6, lobby_match = the_match.match_id)
        commit()

        #asociamos los players

        the_player1.player_lobby = the_lobby.lobby_id
        the_player1.player_current_match_id = the_match.match_id

        the_player2.player_lobby = the_lobby.lobby_id
        the_player2.player_current_match_id = the_match.match_id

        the_player3.player_lobby = the_lobby.lobby_id
        the_player3.player_current_match_id = the_match.match_id

        the_player4.player_lobby = the_lobby.lobby_id
        the_player4.player_current_match_id = the_match.match_id

        the_player5.player_lobby = the_lobby.lobby_id
        the_player5.player_current_match_id = the_match.match_id

        the_player6.player_lobby = the_lobby.lobby_id
        the_player6.player_current_match_id = the_match.match_id

        the_lobby.lobby_match = the_match
        commit()