
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
        return False
    player_counter = cause.player_lobby.lobby_pcount

    cause_position = cause.player_position
    target_position = target.player_position
    if (target.player_dead == True):
        return False

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

    return left == target_position   or right == target_position

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
    def aplicar_efecto(objective_id,player_cause_id): #se añade pĺayer_id para indicar el jugador que causo la jugada
        pass

    @abstractmethod
    def aplay_defense_effect(defensor_id, attacker_id):
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

        # cuando se implemente cuarentena remplazar que revice si el player_cause esta en cuarentena
        in_quarantine = False 

        return is_adjacent and (not in_quarantine)
    

    @db_session
    def aplicar_efecto(self,objective_id,player_cause_id):
        objective_player = Player.get(player_id = objective_id)
        objective_player.player_dead = True
        commit()
        return []
        
    def aplay_defense_effect(self,defensor_id, attacker_id):
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
    def aplicar_efecto(self,objective_id,player_cause_id):
        return []

    def aplay_defense_effect(self,defensor_id, attacker_id):
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
    def aplicar_efecto(self,objective_id,player_cause_id):
        
        return []

    @db_session
    def aplay_defense_effect(self,defensor_id, attacker_id):
        objective_player = Player.get(player_id = defensor_id)
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
        
        return adjacent_players(player_cause_id, target_id)
    
    @db_session
    def aplicar_efecto(self,target_id,player_cause_id):
        player_target = Player.get(player_id = target_id)
        deck_cards = Card.select(lambda c : c.card_player.player_id == target_id).random(1)[0]
        return [deck_cards.card_cardT.cardT_name]
    
    def aplay_defense_effect(self,defensor_id, attacker_id):
        return True
    
    def fullfile_efect(self,target_id):
        return True

    
analisis_effect = "Muestra todas las cartas del jugador adyacente"

class Analisis(card_template):
    def __init__(self):
        super().__init__(False,cards_subtypes.ACTION.value,sospecha_effect,"analisis")
    
    def valid_play(self, player_cause_id,target_id):
        pass
    #MODIFICAR 
    @db_session
    def aplicar_efecto(self,target_id,player_cause_id):
        pass
        '''
        target_hand = []
        player_cause = Player.get(player_id = player_cause_id)
        check_target = isValidTarget(player_cause_id, target_id)
        if check_target == False:
            mensaje= "El jugador no existe"
            return JSONResponse(content=mensaje, status_code=404)

        target_player_cards = list(target_player.player_cards)
        for cards in target_player_cards:
            target_hand.append(cards.card_cardT.cardT_name)
        mensaje = f"Las cartas que tiene {player_cause.player_name} son :{target_hand}"
        return JSONResponse(content= mensaje, status_code=200)
        '''


cambioDeLugar_effect = "Cámbiate de sitio físicamente con un jugador que tengas al lado,salvo que te lo impida un obstáculo como Cuarentena o “Puerta atrancada"

class CambioDeLugar(card_template):

    def __init__(self):
        super().__init__(False,cards_subtypes.ACTION.value,cambioDeLugar_effect,"cambio_de_lugar")
    
    #si no hya condiciones necesarias para jugar la carta, devuelve false o true
    @db_session
    def valid_play(self,player_cause_id,target_id): 
        
        is_adjacent = adjacent_players(player_cause_id, target_id)

        someone_in_quarantine = False # cuando este implementada cuarentena modificar por un metodo
                                        # que detecte si algun jugador esta en cuarentena    

        locked_door = False # cuando este implementada puerta atrancada modificar por un metodo que detecte 
                            # si hay una puerta atrancada en medio    
        return is_adjacent and (not someone_in_quarantine) and (not locked_door) 

    #se añade pĺayer_id para indicar el jugador que causo la jugada
    @db_session
    def aplicar_efecto(self,objective_id,player_cause_id): 
        target = Player.get(player_id = objective_id)        
        cause = Player.get(player_id = player_cause_id)

        target_old_pos = target.player_position
        target.player_position = cause.player_position
        cause.player_position = target_old_pos
        commit()

        return []
    
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
    def aplicar_efecto(self,objective_id,player_cause_id): 
        target = Player.get(player_id = objective_id)        

        target_match = target.player_current_match_id
        match = Match.get(match_id = target_match.match_id)
        match.match_direction = not(match.match_direction)

        commit()

        return []

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
    def aplicar_efecto(self,objective_id,player_cause_id): 
        target = Player.get(player_id = objective_id)        
        cause = Player.get(player_id = player_cause_id)

        target_old_pos = target.player_position
        target.player_position = cause.player_position
        cause.player_position = target_old_pos
        commit()

        return []