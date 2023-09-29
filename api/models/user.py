from pydantic import *
from enum import Enum
from typing import Optional, List, Any
from api.models.item import *
from fastapi import FastAPI, HTTPException, APIRouter, Query
from fastapi.responses import JSONResponse
from pony.orm import db_session, commit 

from db.db_la_cosaP import Player as db_player

router = APIRouter()

class Roles(int, Enum):
    THE_THING = 1
    HUMAN = 2
    INFECTED = 3

class Player(BaseModel):
    player_name: str
    ingame: Optional[bool] = False
    role: Optional[Roles] = None 
    exchangeL: Optional[bool] = True
    exchangeR: Optional[bool] = True
    position: Optional[int] = None
    dead: Optional[bool] = False
    cards: List[Card] = None
    lobby: Optional[Lobby] = None
    isHost: Optional[bool] = True # ojo que por defecto es host


class PlayerOut(BaseModel):
    player_id : int
    player_name : str


 

@router.post("/players", response_model=PlayerOut)
async def crear_jugador(new_player: Player, name : str) -> Any:
    if len(name) > 20: #FALTAN VALIDAR LOS CAMPOS DE PLAYER
            message = "Nombe demasiado largo"
            status_code = 406 # no acceptable
            return JSONResponse(content=message, status_code=status_code)
    with db_session:
        new_player = db_player(player_name= name, player_ingame = False, player_isHost=False)
        commit()
    return new_player



        
