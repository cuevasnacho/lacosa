
from pydantic import *
from api.card.alejate import *
from pony.orm import db_session, commit
from db.database import CardTemplate as db_cardT

lanzallamas = lanzallamas_T()
la_cosa = laCosa_T()
nada_de_barbacoas = NadaDeBarbacoa()
sospecha = Sospecha()
analisis = Analisis()
vigila_tus_espaldas = VigilaTusEspaldas()
cambio_de_lugar = CambioDeLugar()
mas_vale_que_corras = MasValeQueCorras()
whisky = Whisky()
puerta_atrancada = PuertaAtrancada()
aqui_estoy_bien = AquiEstoyBien()
infectado = Infectado()
aterrador = Aterrador()
cuarentena = Cuarentena()
hacha = Hacha()
seduccion = Seduccion()
revelaciones = Revelaciones()
cita_a_ciegas = CitaACiegas()
no_gracias = NoGracias()
que_quede_entre_nosotros = QueQuedeEntreNosotros()
fallaste = Fallaste()
ups = Ups()

Template_Diccionary = {
    "lanzallamas" : lanzallamas,
    "lacosa"     : la_cosa,
    "nada_de_barbacoas" : nada_de_barbacoas,
    "sospecha" : sospecha,
    "analisis" : analisis,
    "cambio_de_lugar" : cambio_de_lugar,
    "vigila_tus_espaldas" : vigila_tus_espaldas,
    "mas_vale_que_corras" : mas_vale_que_corras,
    "whisky" : whisky,
    "puerta_atrancada" : puerta_atrancada,
    "aterrador" : aterrador,
    "aqui_estoy_bien" : aqui_estoy_bien,
    "infectado" : infectado,
    "cuarentena" : cuarentena,
    "hacha" : hacha,
    "seduccion" : seduccion,
    "revelaciones" : revelaciones,
    "no_gracias" : no_gracias,
    "cita_a_ciegas" : cita_a_ciegas,
    "fallaste" : fallaste,
    "ups" : ups
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
    
