
from pydantic import *
from api.alejate import *
from pony.orm import db_session, commit , ObjectNotFound
from pony.orm import Set, exists
from db.database import CardTemplate as db_cardT

from enum import Enum

class desck_creation(Enum):
    SUCSSESFUL = 1
    ERROR = 0


lanzallamas = lanzallamas_T()
la_cosa = laCosa_T()

Template_Diccionary = {
    "Lanzallamas" : lanzallamas,
    "La_Cosa"     : la_cosa
}

def already_load(name):
    with db_session:
        return db_cardT.exists(cardT_name = name) 


@db_session
def load_templates():

    try:

        for key in Template_Diccionary :
            if(not(already_load(key))):
                baseTemp = Template_Diccionary[key]
                new_template= db_cardT(cardT_subtype = baseTemp.alejate_type,
                                       cardT_type = baseTemp.type,
                                       cardT_effect = baseTemp.effect,
                                       cardT_name = baseTemp.name)
        
        commit() #genera todas las inserciones juntas

        return True #ok
    
    except Exception as e:
        print(f"Error durante la carga de las plantillas: {e}")
        return False  # Fallo
    