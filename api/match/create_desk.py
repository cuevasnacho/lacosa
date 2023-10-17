
from pony.orm import db_session, commit , ObjectNotFound, select
from db.database import Card as db_card
from db.database import CardTemplate as db_cardT
from db.database import Match
from definitions import card_position, results

from enum import Enum


AMOUNT_PER_NUMBER = 20

@db_session
def generate_cards(number,id_match,template):
    try:
        match = Match.get(match_id = id_match)
        for i in range(0,AMOUNT_PER_NUMBER):
            new_Card = db_card(card_location =card_position.DECK.value,
                                card_number = number,
                                card_cardT = template,
                                card_match = id_match)
            match.match_cardsCount += 1
            commit()
    except Exception as e:
        print(f"Error al crear el mazo: {e}")                
        return results.ERROR.value


@db_session
def create_desk(players_amount,id_match):

    try:
        List_of_templates = select(template for template in db_cardT)[:]

        match = Match.get(match_id = id_match)

        for template in List_of_templates:
                if(template.cardT_name =="lacosa"):
                    #el card number es 0 porque es la carta la cosa
                    new_Card = db_card(card_location =card_position.DECK.value,
                                        card_number = 0,
                                        card_cardT = template,
                                        card_match = id_match)
                    match.match_cardsCount += 1
                    commit()
                else:
                    for number in range(4,players_amount+1):
                        generate_cards(number,id_match,template)
        return results.SUCSSESFUL.value
    except Exception as e:
        print(f"Error al crear el mazo: {e}")
        return results.ERROR.value


#insert into Match (match_id, match_status, match_direction, match_currentP, match_cardsCount) VALUES (2,0,0,0,0);
