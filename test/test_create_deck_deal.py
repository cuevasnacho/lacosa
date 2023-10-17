import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from main import app 
from pony.orm import db_session, delete, commit,flush, rollback
from definitions import card_position,player_roles
import json 
import os 
import subprocess
import time 
from db.database import db,Player, Lobby, Match, CardTemplate, Card
from api.match.deal_cards import deal_cards
from api.match.create_desk import *



fileEntrys = ["db/deal_create.txt"]

def reset_and_load_database(to_load):
    database = "db/lacosa.sqlite"
    create_database_command = "python3 db/database.py"
    get_into_database = "sqlite3 db/lacosa.sqlite"
    file_entrys = to_load
    if os.path.exists(database):
        db.drop_all_tables(with_all_data=True)  
              
    subprocess.run(create_database_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(0.1)
    
    try:
        # Start a transaction
        with db_session:
            with open(file_entrys, 'r') as file:
                # Iterate over each line of the file
                for line in file:
                    # Process the line, for example, printing it in the console
                    command = get_into_database + " " + line.strip()
                    print(command)
                    subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    time.sleep(0.1)
            # Commit the changes made during the transaction
            commit()
    except Exception as e:
        # Handle exceptions, possibly rollback changes
        print(f"Error during database reset and load: {e}")
        rollback()

def test_create_deck_deal():
    reset_and_load_database(fileEntrys[0])
    id_match = 2

    with db_session:
        match = Match.get(match_id = id_match)
        amount_players = match.match_lobby.lobby_pcount

        cards_related =  Card.select(lambda card: card.card_match.match_id == id_match and
                                    card.card_location == card_position.DECK.value).count()

        assert cards_related == match.match_cardsCount

    create_desk(amount_players, id_match)

    with db_session:
        match = Match.get(match_id = id_match)

        templeates_amount = CardTemplate.select().count()

        cards_related = Card.select(lambda card: card.card_match.match_id == id_match and
                                    card.card_location == card_position.DECK.value).count()
        lacosa_amount = Card.select(lambda card: card.card_match.match_id == id_match and
                                    card.card_location == card_position.DECK.value and
                                    card.card_cardT.cardT_name == "lacosa").count()

        expected = (templeates_amount-1)*AMOUNT_PER_NUMBER *(amount_players-3) +1

        assert cards_related == match.match_cardsCount
        assert match.match_cardsCount == expected
        assert lacosa_amount == 1

    deal_cards(id_match)
    with db_session:
        match = Match.get(match_id = id_match)

        cards_related = Card.select(lambda card: card.card_match.match_id == id_match and
                                    card.card_location == card_position.DECK.value).count()
        lacosa_amount = Card.select(lambda card: card.card_match.match_id == id_match and
                                    card.card_location == card_position.DECK.value and
                                    card.card_cardT.cardT_name == "lacosa").count()

        expected = expected - (amount_players *4)

        assert cards_related == match.match_cardsCount
        assert match.match_cardsCount == expected
        assert lacosa_amount == 0

        players = list(match.match_players)

        lacosa_amount = 0
        for player in players:
            cards = list(player.player_cards)
            assert len(cards) == 4

            for card in cards :
                assert card.card_location == card_position.PLAYER.value
                assert card.card_player == player
                if(card.card_cardT.cardT_name == "lacosa"):
                    assert player.player_role == player_roles.THE_THING.value
                    lacosa_amount +=1

        assert lacosa_amount == 1