
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


def fullfile_action(defensor_id, attack_card_name):
    card_used = Template_Diccionary[attack_card_name]
    card_used.fullfile_efect(defensor_id)

def cita_a_ciegas_fullfile(player_id,selected_card_id):
    exchange_card_not_panic(player_id,selected_card_id)