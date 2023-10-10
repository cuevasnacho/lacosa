
from pony.orm import db_session, commit
from db.database import Player
from definitions import cards_subtypes
from fastapi.responses import JSONResponse

from abc import ABC, abstractmethod


class card_template(ABC):
    def __init__(self,isPanic,alejate_type,effect,name) -> None:
        self.type = isPanic
        self.alejate_type = alejate_type
        self.effect = effect
        self.name = name

    @abstractmethod
    def aplicar_efecto(objective_id):
        pass

lanz_Effect = "Eliminar el jugador objetivo"

class lanzallamas_T(card_template):
    def __init__(self):
        super().__init__(False, cards_subtypes.ACTION.value,lanz_Effect,"lanzallamas")

    @db_session
    def aplicar_efecto(self,objective_id):
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
    def aplicar_efecto(self,objective_id):
        message = "Accion invalida"
        return JSONResponse(content = message, status_code=406)


nada_de_barbacoas_effect = "Anula carta Lanzallamas"

class NadaDeBarbacoa(card_template):
    def __init__(self):
        super().__init__(False,cards_subtypes.DEFENSE.value,nada_de_barbacoas_effect,"nada_de_barbacoas")
    
    @db_session
    def aplicar_efecto(self,objective_id):
        objective_player = Player.get(player_id = objective_id)
        objective_player.player_dead = False
        commit()