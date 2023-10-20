
import random
from db.database import Player, Match, Card,Lobby
from pony.orm import db_session,commit, select,desc
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from definitions import card_position,cards_subtypes,results, player_roles

router = APIRouter()

@db_session
def deal_cards(id_match):
    try:
        match = Match.get(match_id = id_match)
        lobby = Lobby.get(lobby_id = match.match_id)
        players_amount = lobby.lobby_pcount


        cards_to_deal_query = Card.select(lambda card: card.card_match.match_id == id_match and
                                    not(card.card_cardT.cardT_type) and
                                    card.card_cardT.cardT_subtype != cards_subtypes.INFECTION.value).random((players_amount*4)-1)

        cards_list = list(cards_to_deal_query)

        la_cosa = Card.select(lambda card : card.card_match.match_id == id_match and 
                              card.card_cardT.cardT_name == "lacosa").first()

        cards_list.append(la_cosa)

        players_in_match = list(match.match_players)

        for player in players_in_match:
            for i in range(0,4):
                card = random.choice(cards_list)
                cards_list.remove(card)
                card.card_player = player.player_id
                card.card_location = card_position.PLAYER.value
                if card.card_cardT.cardT_name == "lacosa":
                    player.player_role = player_roles.THE_THING.value

        match.match_cardsCount -= players_amount * 4 
        commit()
        return results.SUCSSESFUL.value #resultado exitoso

    except Exception as e:
        print(f"Error al repartir las cartas: {e}")
        return results.ERROR.value   #Fallo de repartir cartas

