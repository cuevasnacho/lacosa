#es importante tener actalizado el lobby_pcount
from db.database import Lobby, Match
from pony.orm import db_session, commit
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from definitions import match_status
from pony import orm 
from . import Create_Desk
from . import deal_cards
router = APIRouter()

@db_session
def check_pre_conditions(lobby_id):
    try:
        #lobby existe y cumple restriccion cantidad de jugadores
        get_lobby = Lobby.select(lambda lobby : lobby.lobby_id == lobby_id 
                                 and lobby.lobby_pcount <= lobby.lobby_max 
                                 and lobby.lobby_min <= lobby.lobby_pcount).first()
        
        #estado lobby es no inicializado
        is_match_not_initialized = orm.select( (lobby, match)
                                   for match in Match for lobby in Lobby
                                        if lobby.lobby_match.match_id == match.match_id
                                        and lobby.lobby_id == lobby_id
                                        and match.match_status == match_status.NOT_INITIALIZED.value).first()
        
        return True if (get_lobby and is_match_not_initialized) else False
    except:
        return False

@db_session
def get_match_id(lobby_id):
    match_id = orm.select( (match.match_id) 
                for match in Match for lobby in Lobby 
                if lobby.lobby_match.match_id == match.match_id and lobby.lobby_id == lobby_id).first()
    return match_id


@db_session
def get_player_number(id_lobby):
    get_lobby = Lobby.get(lobby_id = id_lobby)
    return get_lobby.lobby_pcount
    
@db_session
def change_match_status(lobby_id):
    match_id = get_match_id(lobby_id)
    get_match = Match.get(match_id = match_id)
    get_match.match_status = match_status.INITIALIZED.value                
    commit()

@router.put("/partida/iniciar/{lobby_id}")
async def start_match(lobby_id : int):
    if (check_pre_conditions(lobby_id)):
        #cambiar estado de match a inicializado
        change_match_status(lobby_id)
        
        #asociar un mazo
        number_players = get_player_number(lobby_id)
        match_id = get_match_id(lobby_id)
        Create_Desk.create_desk(number_players, match_id)

        #repartir cartas
        deal_cards.deal_cards(match_id)

        content = f"Partida {lobby_id} iniciada"
        return JSONResponse(content = content, status_code = 200)
    else:
        content = f"Lobby {lobby_id} no cumple las pre-condiciones"
        return JSONResponse(content = content, status_code = 405)
