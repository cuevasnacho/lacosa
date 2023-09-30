from pony.orm import Database, PrimaryKey, Required, Set, Optional
from pony import *

db = Database()

class Player(db.Entity):
    player_id = PrimaryKey(int, auto=True)
    player_name = Required(str)
    player_ingame = Required(bool)
    player_position = Optional(int)
    player_exchangeR = Optional(bool)
    player_exchangeL= Optional(bool)
    player_role = Optional(int)
    player_dead= Optional(bool)
    player_isHost = Required(bool)

    player_cards = Set("Card", nullable =True)
    player_lobby = Optional("Lobby")
    player_current_match_id = Optional("Match")

class Lobby (db.Entity):
    lobby_id = PrimaryKey(int, auto=True)
    lobby_name = Required(str)
    lobby_max = Required(int)
    lobby_min= Required(int)
    lobby_password = Optional(str, nullable=True)
    lobby_pcount = Required(int)

    lobby_match = Optional("Match")
    lobby_player = Set("Player")

class Match (db.Entity):
    match_id = PrimaryKey(int, auto=True)
    match_status = Required(int)
    match_direction = Required(bool)
    match_currentP = Required(int)
    match_cardsCount= Required(int)

    match_lobby = Required("Lobby")
    match_cards = Set("Card")
    match_players = Set("Player")

class CardTemplate (db.Entity):
    cardT_id = PrimaryKey(int, auto=True)
    cardT_type = Required(bool)
    cardT_subtype = Required(int)
    cardT_effect= Required(str)
    cardT_name = Required(str)

    cardT_card = Set("Card")

class Card (db.Entity):
    card_id = PrimaryKey(int, auto = True)
    card_location = Required(int)
    card_number = Required(int)
    card_cardT = Required("CardTemplate")

    card_player = Optional("Player")
    card_match = Required("Match")


#conectamos el objeto `db` con la base de dato.
db.bind('sqlite', 'lacosa.sqlite', create_db=True)
#generamos las base de datos.
db.generate_mapping(create_tables=True)
