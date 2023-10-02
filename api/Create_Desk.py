
from pony.orm import db_session, commit , ObjectNotFound, select
from db.database import Card as db_card
from db.database import CardTemplate as db_cardT
from definitions import card_position, results

from enum import Enum


AMOUNT_PER_NUMBER = 20

@db_session
def generate_cards(number,match_id,template):
    try:
        for i in range(0,AMOUNT_PER_NUMBER):
            new_Card = db_card(card_location =card_position.DECK.value,
                                card_number = number,
                                card_cardT = template,
                                card_match = match_id)
    except Exception as e:
        print(f"Error al crear el mazo: {e}")                
        return results.ERROR.value


@db_session
def create_desk(players_amount,match_id):

    try:
        List_of_templates = select(template for template in db_cardT)[:]

        for template in List_of_templates:
                
                if(template.cardT_name =="La_Cosa"):
                    #el card number es 0 porque es la carta la cosa
                    new_Card = db_card(card_location =card_position.DECK.value,
                                        card_number = 0,
                                        card_cardT = template,
                                        card_match = match_id)
                    commit()
                else:
                    for number in range(4,players_amount+1):
                        generate_cards(number,match_id,template)
        return results.SUCSSESFUL.value
    except Exception as e:
        print(f"Error al crear el mazo: {e}")
        return results.ERROR.value


#insert into Match (match_id, match_status, match_direction, match_currentP, match_cardsCount) VALUES (2,0,0,0,0);
