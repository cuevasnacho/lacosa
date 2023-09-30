from pydantic import *
from enum import Enum
from typing import Optional, List, Any
from api.models.user import Player
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

