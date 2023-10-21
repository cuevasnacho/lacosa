
from db.database import Card, CardTemplate, Player, Match
from pony.orm import db_session
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.card.load_templates import Template_Diccionary
from api.card.alejate import *
from pony import orm 
from definitions import cards_subtypes
from pydantic import BaseModel
import json 
from typing import List
from definitions import player_roles

def fullfile_action(defensor_id, card_used):
    return True