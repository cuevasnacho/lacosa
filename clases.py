from datetime import datetime
from pony.orm import (Database, PrimaryKey, Required, Set, Optional)


db = Database()


class Jugador(db.Entity):
    player_id = PrimaryKey(int, auto=True)
    nombre_player = Required(str)
    en_partida = Required(bool)
    posicion_mesa = Optional(int)
    intercambiar_D = Optional(bool)
    intercambiar_I = Optional(bool)
    rol = Optional(int)
    eliminado = Optional(bool)

class Lobby(db.Entity):
    lobby_id = PrimaryKey(int, auto=True)
    max_players = Required(int)
    min_players = Required(int)
    passw = Optional(str)
    cant_jugadores = Required(int)

class Partida (db.Entity):
    partida_id = PrimaryKey(int, auto=True)
    estado = Required(int)
    sentido = Optional(bool)
    jugador_de_turno = Optional(int)
    cartas_disponibles = Optional(int)

class CardTemplate (db.Entity):
    tipo = Required(str)
    subtipo = Required(str)
    efecto = Required(str)
    nombre_carta = Required(str)

class Card (CardTemplate):
    id_carta = PrimaryKey(int, auto = True)
    ubicacion = Optional(int)
    numero = Required(int)



# db.generate_mapping()
# Configuramos la base de datos.
# Más info: https://docs.ponyorm.org/database.html

# Conectamos el objeto `db` con la base de dato.
db.bind('sqlite', 'example.sqlite', create_db=True)
# Generamos las base de datos.
db.generate_mapping(create_tables=True)
