from typing import List
import enum
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Column, create_engine, Enum, SmallInteger, Boolean, Text, Table
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



lobby_player_assoc = Table(
    "Players_in_lobby",
    Base.metadata,
    Column("lobby_id", Integer, ForeignKey("Lobby.lobby_id")),
    Column("player_id", Integer, ForeignKey("Player.player_id"))
)
class Roles(enum.Enum):
    THE_THING = 1
    HUMAN = 2
    INFECTED = 3

class Status (enum.Enum):
    NOT_INITIALIZED = 1
    INITIALIZED= 2
    FINISHED = 3

class SubTypes(enum.Enum):
    INFECTION = 1
    ACTION = 2
    DEFENSE = 3
    OBSTACLE = 4

class Locations (enum.Enum):
    IN_DECK = 1
    IN_DISCARD = 2
    IN_PLAYER = 3


class Player(Base):
    __tablename__ = "Player"

    player_id = Column("player_id", Integer, primary_key=True, autoincrement=True)
    player_name = Column("name", String(length=30))
    player_ingame = Column("ingame", Boolean, default=False)
    player_position = Column("position", SmallInteger, nullable=True)
    player_exchangeR = Column("exchangeR", Boolean, default=True )
    player_exchangeL = Column("exchangeL", Boolean, default=True )
    player_role = Column("role", Enum(Roles), nullable=True)
    player_dead = Column("isDead", Boolean, default=False)


    player_cards= relationship("Card", back_populates ="Player")
    player_lobby = relationship("Lobby", secondary=lobby_player_assoc ,back_populates="Player")

    def __init__(self, name, ingame, position, exchangeR, exchangeL, role, dead):
        self.player_id = id
        self.player_name = name
        self.player_ingame = ingame
        self.player_position = position
        self.player_exchangeR = exchangeR
        self.player_exchangeL = exchangeL
        if role in Roles:
            self.player_role = role
        else:
            raise ValueError("Rol no Valido")
        self.player_dead = dead


class Match(Base):
    __tablename__= "Match"
    match_id = Column("match_id", Integer, primary_key=True, autoincrement=True)
    match_status = Column("status", Enum(Status), default=1)
    match_direction = Column("direction", Boolean, default=True) #esto significa que por defecto gira a la izquierda
    match_currentP = Column ("player_turn", Integer, nullable=True)
    match_cards = Column ("deck_count", SmallInteger, default=0)


    match_lobby = relationship("Lobby", back_populates="Match")
    match_cards = relationship("Cards", back_populates="Match", cascade="all, delete-orphan")

    def __init__(self, status, direction, players, cards):
        if status in Estados:
            self.player_role = role
        else:
            raise ValueError("Estado no Valido")
        self.match_status= status
        self.match_direction = direction
        self.match_currentP = players
        self.match_cards = cards


class Lobby(Base):
    __tablename__= "Lobby"
    lobby_id = Column("lobby_id", Integer, primary_key=True, autoincrement=True )
    lobby_name = Column("name", String(length=30), nullable=False)
    lobby_max = Column("max_players", SmallInteger, default=12)
    lobby_min = Column("min_players", SmallInteger, default=5)
    lobby_password = Column("password", String(length=12), nullable=True)
    lobby_pcount = Column("current_players", SmallInteger, default=1)


    lobby_match = relationship("Match", uselist=False, back_populates="Lobby", cascade="all, delete-orphan")
    lobby_player = relationship("Lobby", secondary=lobby_player_assoc, back_populates="Player")

    def __init__(self, name, max, min, password, players):
        self.lobby_name = name
        self.lobby_max = max
        self.lobby_min = min
        self.lobby_password = password
        self.lobby_pcount= players

class CardTemplate (Base):
    __tablename__="Template"
    cardT_id = Column("id", Integer, primary_key=True, autoincrement=True )
    cardT_type = Column("Type", Boolean, nullable=False) #como son dos tipos Alejate=1 y Panico = 0
    cardT_subtype = Column("Subtype", Enum(SubTypes), nullable=False)
    cardT_effect = Column("Effect", Text, nullable=False)
    cardT_name = Column("Name", String, nullable=False)


    cardT_card = relationship("Cards", back_populates="Template")

    def __init__(self, cardtype, subtype, effect, name):
        self.cardT_type = cardtype
        if subtype in SubTypes:
            self.cardT_subtype= subtype
        else: 
            raise ValueError("Subitpo no valido")
        self.cardT_effect = effect
        self.cardT_name = name



class Card (Base):
    __tablename__="Card"

    card_id = Column("id", Integer, primary_key=True, autoincrement=True)
    card_location = Column("Locations", Enum(Locations), nullable=True) #null para casos en que la carta no fue usada para la Match
    card_number = Column("Number", SmallInteger)
    card_player = Column(Integer, ForeignKey("Player.player_id"), nullable=True)


    card_match = relationship("Match", back_populates="Card")
    player = relationship("Player", back_populates="Card")
    card_template = relationship("CardTemplate", back_populates="Cards")

    def __init__(self, location, number, belongs):
        if ubicacion in Ubicaciones:
            self.card_location= location
        else:
            raise ValueError("Ubicacion no valida")
        self.card_number = number
        self.card_player = belongs
        


db = "sqlite:///clases.db"
engine= create_engine(db, echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session= Session()