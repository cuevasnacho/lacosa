
from pony.orm import db_session, commit
from db.database import Player,Card,Match
from definitions import cards_subtypes, card_position
from fastapi.responses import JSONResponse
import random
from abc import ABC, abstractmethod

#chequa que el jugador sea alguno del costado
@db_session
def adjacent_players(player_cause_id,target_id):
    cause = Player.get(player_id = player_cause_id)
    target = Player.get(player_id = target_id)
    match_id = cause.player_current_match_id.match_id
    if cause == None or target== None:
        return None
    player_counter = cause.player_lobby.lobby_pcount

    cause_position = cause.player_position
    target_position = target.player_position
    if (target.player_dead == True):
        return (False,False)

    left = (cause_position - 1) % player_counter 
    right = (cause_position + 1) % player_counter
    player_left = Player.select (lambda p: p.player_current_match_id.match_id == match_id and p.player_position == left).first()
    player_right = Player.select (lambda p: p.player_current_match_id.match_id == match_id and p.player_position == right).first()
    while player_left.player_dead == True:
        left = (left - 1) % player_counter
        player_left = Player.select (lambda p: p.player_current_match_id.match_id == match_id and p.player_position == left).first()
    while player_right.player_dead == True:
        right = (right + 1) % player_counter
        player_right = Player.select (lambda p: p.player_current_match_id.match_id == match_id and p.player_position == right).first()

    return (left == target_position, right == target_position)

@db_session
def swap_doors(player_id_1,player_id_2):
    p1 = Player[player_id_1]
    p2 = Player[player_id_2]

    aux_left = p1.player_exchangeL
    aux_rigth = p1.player_exchangeR
    
    p1.player_exchangeL = p2.player_exchangeL
    p1.player_exchangeR = p2.player_exchangeR
    
    p2.player_exchangeL = aux_left
    p2.player_exchangeR = aux_rigth

    commit()

def get_card_not_panic(match_id):
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
def exchange_card_not_panic(player_id,card_id):
    player = Player.get(player_id = player_id)
    match = player.player_current_match_id
    selected_card = Card.get(card_id = card_id)

    card = get_card_not_panic(match.match_id)

    card.card_location = card_position.PLAYER.value
    selected_card.card_location = card_position.DECK.value

    card.card_player = player
    commit()


class card_template(ABC):
    def __init__(self,isPanic,alejate_type,effect,name) -> None:
        self.type = isPanic
        self.alejate_type = alejate_type
        self.effect = effect
        self.name = name
    @abstractmethod
    def valid_play(player_cause_id,target_id): #si no hya condiciones necesarias para jugar la carta, devuelve false o true
        pass

    @abstractmethod
    def aplicar_efecto(objective_id,player_cause_id,card_id): #se añade pĺayer_id para indicar el jugador que causo la jugada
        pass

    @abstractmethod
    def aplay_defense_effect(defensor_id, attacker_id,card_id):
        pass

    @abstractmethod
    def fullfile_efect(target_id):
        pass

lanz_Effdect = "Eliminar el jugador objetivo"

class lanzallamas_T(card_template):
    def __init__(self):
        super().__init__(False, cards_subtypes.ACTION.value,lanz_Effdect,"lanzallamas")
    @db_session
    def valid_play(self, player_cause_id,target_id):

        is_adjacent = adjacent_players(player_cause_id, target_id)
        valid = is_adjacent[0] or is_adjacent[1]

        player = Player[player_cause_id]
        if player.player_quarentine_count > 0:
            return False

        return valid
    

    @db_session
    def aplicar_efecto(self,objective_id,player_cause_id,card_id):
        
        objective_player = Player[objective_id]
        cause_player = Player[player_cause_id]
        
        side = adjacent_players(player_cause_id,objective_id)
        
        if side[0]:
            cause_player.player_exchangeL = objective_player.player_exchangeL 
        elif side[1]:
            cause_player.player_exchangeR = objective_player.player_exchangeR

        objective_player.player_dead = True

        commit()
        return []
        
    def aplay_defense_effect(self,defensor_id, attacker_id,card_id):
        return True
    
    @db_session
    def fullfile_efect(self,target_id):
        
        target = Player.get(player_id = target_id)

        target_hand = list(target.player_cards)

        for card in target_hand:
            card.card_location = card_position.DISCARD.value
            card.card_player = None

        commit()
        return True

cosa_Effect = "something"

class laCosa_T(card_template):

    def __init__(self):
        super().__init__(False, cards_subtypes.INFECTION.value,cosa_Effect,"lacosa")
    def valid_play(self, player_cause_id,target_id):
        return False

    @db_session
    def aplicar_efecto(self,objective_id,player_cause_id,card_id):
        return []

    def aplay_defense_effect(self,defensor_id, attacker_id,card_id):
        pass
    
    def fullfile_efect(self,target_id):
        pass


nada_de_barbacoas_effect = "Anula carta Lanzallamas"

class NadaDeBarbacoa(card_template):
    def __init__(self):
        super().__init__(False,cards_subtypes.DEFENSE.value,nada_de_barbacoas_effect,"nada_de_barbacoas")

    def valid_play(self, player_cause_id,target_id):
        return True
    
    @db_session
    def aplicar_efecto(self,objective_id,player_cause_id,card_id):
        
        return []

    @db_session
    def aplay_defense_effect(self,defensor_id, attacker_id,card_id):
        attacker = Player[attacker_id]
        objective_player = Player[defensor_id]
        
        side = adjacent_players(attacker_id,defensor_id)
        
        if side[0]:
            attacker.player_exchangeL = True 
        elif side[1]:
            attacker.player_exchangeR = True
        
        objective_player.player_dead = False

        commit()
        return True
    
    def fullfile_efect(self,target_id):
        return True


sospecha_effect = "Muestra carta aleatoria de un jugador adyacente"

class Sospecha(card_template):
    def __init__(self):
        super().__init__(False,cards_subtypes.ACTION.value,sospecha_effect,"sospecha")
    
    @db_session
    def valid_play(self,player_cause_id,target_id):

        is_adjacent = adjacent_players(player_cause_id, target_id)
        valid = is_adjacent[0] or is_adjacent[1]
        
        return valid
    
    @db_session
    def aplicar_efecto(self,target_id,player_cause_id,card_id):
        player_target = Player.get(player_id = target_id)
        deck_cards = Card.select(lambda c : c.card_player.player_id == target_id).random(1)[0]
        return [deck_cards.card_cardT.cardT_name]
    
    def aplay_defense_effect(self,defensor_id, attacker_id,card_id):
        return True
    
    def fullfile_efect(self,target_id):
        return True

    
analisis_effect = "Muestra todas las cartas del jugador adyacente"

class Analisis(card_template):
    def __init__(self):
        super().__init__(False,cards_subtypes.ACTION.value,sospecha_effect,"analisis")
    
    @db_session
    def valid_play(self, player_cause_id,target_id):
        is_adjacent = adjacent_players(player_cause_id, target_id)
        valid = is_adjacent[0] or is_adjacent[1]
        return valid

    @db_session
    def aplicar_efecto(self,target_id,player_cause_id,card_id):
        target_hand = []
        target_player = Player.get(player_id = target_id)
        target_player_cards = list(target_player.player_cards)
        for cards in target_player_cards:
            target_hand.append(cards.card_cardT.cardT_name)
        return target_hand
        
    def aplay_defense_effect(self,defensor_id, attacker_id,card_id):
        return True
    
    def fullfile_efect(self,target_id):
        return True

    

cambioDeLugar_effect = "Cámbiate de sitio físicamente con un jugador que tengas al lado,salvo que te lo impida un obstáculo como Cuarentena o “Puerta atrancada"

class CambioDeLugar(card_template):

    def __init__(self):
        super().__init__(False,cards_subtypes.ACTION.value,cambioDeLugar_effect,"cambio_de_lugar")
    
    #si no hya condiciones necesarias para jugar la carta, devuelve false o true
    @db_session
    def valid_play(self,player_cause_id,target_id): 
        
        is_adjacent = adjacent_players(player_cause_id, target_id)
        valid = is_adjacent[0] or is_adjacent[1]

        player = Player[player_cause_id]
        if player.player_quarentine_count > 0:
            return False

        locked_door = False # cuando este implementada puerta atrancada modificar por un metodo que detecte 
                            # si hay una puerta atrancada en medio    
        return valid and (not locked_door) 

    #se añade pĺayer_id para indicar el jugador que causo la jugada
    
    def aplicar_efecto(self,objective_id,player_cause_id,card_id): 
        with db_session:    
            target = Player.get(player_id = objective_id)        
            cause = Player.get(player_id = player_cause_id)

            target_old_pos = target.player_position
            target.player_position = cause.player_position
            cause.player_position = target_old_pos
            commit()

        swap_doors(objective_id,player_cause_id)

        return []

    def aplay_defense_effect(self,defensor_id, attacker_id,card_id):
        return True
    
    def fullfile_efect(self,target_id):
        return True
    
vigila_tus_espaldas_effect = "Invierte el orden de juego"

class VigilaTusEspaldas(card_template):

    def __init__(self):
        super().__init__(False,cards_subtypes.ACTION.value,vigila_tus_espaldas_effect,"vigila_tus_espaldas")
    
    #si no hya condiciones necesarias para jugar la carta, devuelve false o true
    @db_session
    def valid_play(self,player_cause_id,target_id): 
        
        return True 
        #player_cause_id == target_id

    #se añade pĺayer_id para indicar el jugador que causo la jugada
    @db_session
    def aplicar_efecto(self,objective_id,player_cause_id,card_id): 
        target = Player.get(player_id = objective_id)        

        target_match = target.player_current_match_id
        match = Match.get(match_id = target_match.match_id)
        match.match_direction = not(match.match_direction)

        commit()

        return []

    def aplay_defense_effect(self,defensor_id, attacker_id,card_id):
        return True
    
    def fullfile_efect(self,target_id):
        return True
    
masValeQueCorras_effect = "Cámbiate de sitio físicamente con cualquier jugador que no esté bajo los efectos de “Cuarentena”"

class MasValeQueCorras(card_template):

    def __init__(self):
        super().__init__(False,cards_subtypes.ACTION.value,masValeQueCorras_effect,"mas_vale_que_corras")
    
    #si no hya condiciones necesarias para jugar la carta, devuelve false o true
    @db_session
    def valid_play(self,player_cause_id,target_id): 
        

        someone_in_quarantine = False # cuando este implementada cuarentena modificar por un metodo
                                        # que detecte si algun jugador esta en cuarentena    

        return not someone_in_quarantine 

    #se añade pĺayer_id para indicar el jugador que causo la jugada
    @db_session
    def aplicar_efecto(self,objective_id,player_cause_id,card_id): 
        with db_session:
            target = Player.get(player_id = objective_id)        
            cause = Player.get(player_id = player_cause_id)

            target_old_pos = target.player_position
            target.player_position = cause.player_position
            cause.player_position = target_old_pos
            commit()

        swap_doors(objective_id,player_cause_id)

        return []
    
    def aplay_defense_effect(self,defensor_id, attacker_id,card_id):
        return True
    
    def fullfile_efect(self,target_id):
        return True
    
whisky_effect = "Enseño mis cartas a todos los jugadores" # Ésta carta solo la puedo jugar sobre mí mismo

class Whisky(card_template):

      def __init__(self):
          super().__init__(False, cards_subtypes.ACTION.value, whisky_effect, "whisky")

      #si no hay condiciones necesarias para jugar la carta, devuelve false o true
      @db_session
      def valid_play(self,player_cause_id,target_id):
          return player_cause_id == target_id

      #se añade pĺayer_id para indicar el jugador que causo la jugada
      @db_session
      def aplicar_efecto(self, objective_id, player_cause_id,card_id):
          player_cause = Player.get(player_id=player_cause_id)
          player_hand = list(player_cause.player_cards)

          revealed_cards = [card.card_cardT.cardT_name for card in player_hand]

          return revealed_cards

      def aplay_defense_effect(self,defensor_id, attacker_id,card_id):
          return True

      def fullfile_efect(self,target_id):
          return True

puertaAtrancada_effect = "No se podra intercambiar, jugar ni robar al jugador que se aplica"


class PuertaAtrancada(card_template):

      def __init__(self):
          super().__init__(False, cards_subtypes.OBSTACLE.value, puertaAtrancada_effect, "puerta_atrancada")

      #si no hay condiciones necesarias para jugar la carta, devuelve false o true
      @db_session
      def valid_play(self,player_cause_id,target_id):
            is_adjacent = adjacent_players(player_cause_id, target_id)
            valid = is_adjacent[0] or is_adjacent[1]
            return valid

      #se añade pĺayer_id para indicar el jugador que causo la jugada
      @db_session
      def aplicar_efecto(self, objective_id, player_cause_id,card_id):
          player_cause = Player.get(player_id=player_cause_id)
          player_objective = Player.get(player_id = objective_id)

          cause_pos = player_cause.player_position
          objective_pos = player_objective.player_position

          left_or_rigth = adjacent_players(player_cause_id, objective_id)

          if left_or_rigth[0]: #esta a la izquierda
            player_cause.player_exchangeL = False
            player_objective.player_exchangeR = False
            commit()

          if left_or_rigth[1]: #esta a la derecha
            player_cause.player_exchangeR = False
            player_objective.player_exchangeL = False
            commit()

          return []

      def aplay_defense_effect(self,defensor_id, attacker_id,card_id):
          return True

      def fullfile_efect(self,target_id):
          return True

aterrador = "Niegate a un intercambio de cartas solicitado por un jugador o por el efecto de una carta. Mira la carta que te has negado a coger y devuélvesela a su dueño."

class Aterrador (card_template):

    def __init__(self):
        super().__init__(False, cards_subtypes.DEFENSE.value, aterrador, "aterrador")


    @db_session
    def valid_play(self,player_cause_id,target_id):
        return False

    @db_session
    def aplicar_efecto(self, objective_id, player_cause_id,card_id):
        return []

    @db_session
    def aplay_defense_effect(self,defensor_id, attacker_id,card_id):

        return ["aterrador"]
        
    def fullfile_efect(self,target_id):
        return True

seduccion_effect = "Intercambia una carta con cualquier jugador que no este en cuarentena"

class Seduccion(card_template):

      def __init__(self):
          super().__init__(False, cards_subtypes.ACTION.value, seduccion_effect, "seduccion")

      @db_session
      def valid_play(self,player_cause_id,target_id):
            player_target = Player.get(player_id = target_id)
            is_in_quarnt = player_target.player_quarentine_count
            if (is_in_quarnt == 0):
                valid = True
            else:
                valid = False 
            return valid

      @db_session
      def aplicar_efecto(self, objective_id, player_cause_id,card_id):
        get_player = Player.get(player_id = player_cause_id)
        match_id = get_player.player_current_match_id.match_id
        motive = "seduccion"
        return [motive]

      def aplay_defense_effect(self,defensor_id, attacker_id,card_id):
          return True

      def fullfile_efect(self,target_id):
          return True

    
cuarentena = "No se podra intercambiar, jugar ni robar al jugador que se aplica"
class Cuarentena(card_template):

    def __init__(self):
        super().__init__(False, cards_subtypes.OBSTACLE.value, cuarentena, "cuarentena")

    @db_session
    def valid_play(self,player_cause_id,target_id):
        is_adjacent = adjacent_players(player_cause_id,target_id)
        valid = is_adjacent[0] or is_adjacent[1]
        return valid 
    
    @db_session
    def aplicar_efecto(self, objective_id, player_cause_id,card_id):
        objective_player = Player.get(player_id = objective_id)
        objective_player.player_quarentine_count = 2
        commit()
        return []

    def aplay_defense_effect(self,defensor_id, attacker_id,card_id):
        return True

    def fullfile_efect(self,target_id):
        return True

hacha_effect = "retira el efecto de puerta atrancada o cuarentena"

class Hacha(card_template):

      def __init__(self):
          super().__init__(False, cards_subtypes.ACTION.value, hacha_effect, "hacha")

      @db_session
      def valid_play(self,player_cause_id,target_id):
            is_adjacent = adjacent_players(player_cause_id, target_id)
            valid = is_adjacent[0] or is_adjacent[1]
            is_self = player_cause_id == target_id
            return valid

      @db_session
      def aplicar_efecto(self, objective_id, player_cause_id,card_id):
        if objective_id == player_cause_id:
            player_cause = Player.get(player_id=player_cause_id)
            if (player_cause.player_quarentine_count > 0):
                player_cause.player_quarentine_count = 0
                commit()
            else:
                player_cause.player_exchangeL = True
                player_cause. player_exchangeR = True
                commit()
        else:
            player_cause = Player.get(player_id=player_cause_id)
            player_objective = Player.get(player_id = objective_id)
            if (player_objective.player_exchangeL or player_objective.player_exchangeR):
                player_objective.player_quarentine_count = 0
                commit()
            else:
                player_cause.player_exchangeL = True
                player_cause. player_exchangeR = True
                commit()
        return []

      def aplay_defense_effect(self,defensor_id, attacker_id,card_id):
          return True

      def fullfile_efect(self,target_id):
          return True


no_gracias = "niegate a un ofrecimiento de intercambio de cartas"




cita_a_ciegas = "Roba una carta del mazo que no sea de panico" #solo se juega sobre si mismo

class   CitaACiegas(card_template):

    def __init__(self):
        super().__init__(True,None, cita_a_ciegas, "cita_a_ciegas")


    @db_session
    def valid_play(self,player_cause_id,target_id):
        return True

    @db_session
    def aplicar_efecto(self, objective_id, player_cause_id,card_id):
        exchange_card_not_panic(player_id,card_id)
        return []

    @db_session
    async def aplay_defense_effect(self,defensor_id, attacker_id,card_id):
        
        return True

    def fullfile_efect(self,target_id):
        return True