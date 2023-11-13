
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

def get_card_not_panic_cAc(match_id):
        deck_cards = Card.select(lambda c : c.card_match.match_id == match_id and
                           c.card_location == card_position.DECK.value and not(c.card_cardT.cardT_type))

        if not deck_cards:
            discard_to_deck(match_id)
            deck_cards = Card.select(lambda c : c.card_match.match_id == match_id and
                           c.card_location == card_position.DECK.value and not(c.card_cardT.cardT_type))

        if deck_cards :
            card_steal = deck_cards.random(1)[0]
            return card_steal


        return deck_cards

@db_session
def exchange_card_not_panic(player_id,selected_card_id):
    player = Player.get(player_id = player_id)
    match = player.player_current_match_id
    selected_card = Card.get(card_id = card_id)

    card = get_card_not_panic_cAc(match.match_id)

    card.card_location = card_position.PLAYER.value
    selected_card.card_location = card_position.DECK.value
    selected_card.card_player = None

    card.card_player = player
    commit()


def fullfile_action(defensor_id, attack_card_name):
    card_used = Template_Diccionary[attack_card_name]
    card_used.fullfile_efect(defensor_id)

def cita_a_ciegas_fullfile(player_id,selected_card_id):
    exchange_card_not_panic(player_id,selecte_card_id)