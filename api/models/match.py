from pydantic import *
from enum import Enum
from typing import Optional, List, Any
from api.models.user import *
from fastapi import FastAPI, HTTPException, APIRouter, Query
from fastapi.responses import JSONResponse
from pony.orm import db_session, commit 
from pony.orm import Set, select
from definitions import match_status

from db.database import Lobby as db_lobby
from db.database import Match as db_match
from db.database import Player as db_player

router = APIRouter()



class Card(BaseModel):
    id: int


class Match(BaseModel):
    match_status : match_status
    match_direction : Optional[bool] = True  #Vamos a a sumir que True=IZQUIERDA, False=DERECHA
    match_currentP : Optional[int]
    match_cardsCount : Optional[int]



# @router.delete("/partidas/{match_id}")
# async def delete_match(match_id: int) :
#     with db_session:
#         try:
#             fetch_match = get_match(match_id)
#             db_match[match_id].delete()
#         except ObjectNotFound:
#             message = "La partida no existe"
#             status_code = 404 # not found
#             return JSONResponse(content=message, status_code=status_code)
#     message = "Partida borrada!"
#     status_code = 200 # no acceptable
#     return JSONResponse(content=message, status_code=status_code)
