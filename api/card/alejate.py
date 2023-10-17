
from pony.orm import db_session, commit
from db.database import Player
from definitions import cards_subtypes
from fastapi.responses import JSONResponse
import random

from abc import ABC, abstractmethod

#metodo solo para comprobar jugadas adyacentes

def isValidTarget(player_cause_id,target_id):
    cause = Player.get(player_id = player_cause_id)
    target = Player.get(player_id = target_id)
    if cause == None or target== None:
        return False
    player_counter = cause.player_lobby.lobby_pcount

    cause_position = cause.player_position
    target_position = target.player_position
    if cause_position -1 % player_counter != target_position or
    cause_position +1 % player_counter != target_position:
        return False
    else: 
        return True



    



class card_template(ABC):
    def __init__(self,isPanic,alejate_type,effect,name) -> None:
        self.type = isPanic
        self.alejate_type = alejate_type
        self.effect = effect
        self.name = name
    @abstractmethod
    def valid_play(objective_id,player_cause_id): #si no hya condiciones necesarias para jugar la carta, devuelve false o true
        pass

    @abstractmethod
    def aplicar_efecto(objective_id,player_cause_id): #se añade pĺayer_id para indicar el jugador que causo la jugada
        pass

lanz_Effdect = "Eliminar el jugador objetivo"

class lanzallamas_T(card_template):
    def __init__(self):
        super().__init__(False, cards_subtypes.ACTION.value,lanz_Effect,"lanzallamas")

    @db_session
    def aplicar_efecto(self,objective_id,player_cause_id):
        objective_player = Player.get(player_id = objective_id)
        objective_player.player_dead = True
        commit()
        message = f"Jugador {objective_player.player_name} eliminado"
        return JSONResponse(content = message, status_code=200)
        
cosa_Effect = "something"

class laCosa_T(card_template):

    def __init__(self):
        super().__init__(False, cards_subtypes.INFECTION.value,cosa_Effect,"lacosa")

    @db_session
    def aplicar_efecto(self,objective_id,player_cause_id):
        message = "Accion invalida"
        return JSONResponse(content = message, status_code=406)


nada_de_barbacoas_effect = "Anula carta Lanzallamas"

class NadaDeBarbacoa(card_template):
    def __init__(self):
        super().__init__(False,cards_subtypes.DEFENSE.value,nada_de_barbacoas_effect,"nada_de_barbacoas")
    
    @db_session
    def aplicar_efecto(self,objective_id,player_cause_id):
        objective_player = Player.get(player_id = objective_id)
        objective_player.player_dead = False
        commit()

sospecha_effect = "Muestra carta aleatoria de un jugador adyacente"

class Sospecha(card_template):
    def __init__(self):
        super().__init__(False,cards_subtypes.ACTION.value,sospecha_effect,"sospecha")
    
    @db_session
    def aplicar_efecto(self,target_id,player_cause_id):
        player_cause = Player.get(player_id = player_cause_id)
        check_target = isValidTarget(player_cause_id, target_id)
        if check_target == False:
            mensaje= "El jugador no existe"
            return JSONResponse(content=mensaje, status_code=404)

        target_player_cards = list(target_player.player_cards)
        random_card = random.choice(target_player_cards)
        mensaje = f"Una de las cartas de su mano es {random_card.card_cardT.cardT_name}"
        return JSONResponse(content= mensaje, status_code=200)
    
analisis_effect = "Muestra todas las cartas del jugador adyacente"

class Analisis(card_template):
    def __init__(self):
        super().__init__(False,cards_subtypes.ACTION.value,sospecha_effect,"analisis")
    
    @db_session
    def aplicar_efecto(self,target_id,player_cause_id):
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



