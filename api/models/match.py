from pydantic import *
from enum import Enum
from typing import Optional, List, Any
from api.models.user import *
from fastapi import FastAPI, HTTPException, APIRouter, Query
from fastapi.responses import JSONResponse
from pony.orm import db_session, commit 
from pony.orm import Set
from definitions import match_status

from db.database import Lobby as db_lobby
from db.database import Match as db_Match
from db.database import Player as db_player

router = APIRouter()



class Card(BaseModel):
    id: int


class Match(BaseModel):
    match_status : match_status
    match_direction : Optional[bool] = True  #Vamos a a sumir que True=IZQUIERDA, False=DERECHA
    match_currentP : Optional[int]
    match_cardsCount : Optional[int]