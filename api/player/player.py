from pydantic import *
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pony.orm import db_session, commit, ObjectNotFound
from db.database import Player as db_player

router = APIRouter()

class PlayerIn(BaseModel):
    player_name: str

class PlayerOut(BaseModel):
    player_id : int
    player_name : str


@db_session()
def get_jugador(player_id):
    try:
        player = db_player[player_id]
        return player
    except ObjectNotFound:
        message = "El jugador no existe"
        status_code = 404 # not found
        return JSONResponse(content=message, status_code=status_code)

@router.post("/players")
async def Crear_Jugador(new_player: PlayerIn) -> PlayerOut:
    if len(new_player.player_name) > 20: 
        message = "Nombe demasiado largo"
        status_code = 406 # no acceptable
        return JSONResponse(content=message, status_code=status_code)
    with db_session:
        player = db_player(player_name= new_player.player_name, player_ingame = False, player_isHost=False, 
                           player_dead = False, player_position = 0, player_exchangeR = 0, player_exchangeL = 0,
                            player_role = 0, player_lobby = None, player_current_match_id = None )
        commit()
        return PlayerOut(player_id=player.player_id, player_name=player.player_name)


@router.get("/players/{player_id}")
async def Buscar_Jugador(player_id : int):
    player =get_jugador(player_id)
    return{
    "player_name": player.player_name,
    "player_ingame": player.player_ingame,
    "player_role": player.player_role,
    "player_exchangeL": player.player_exchangeL,
    "player_exchangeR": player.player_exchangeR,
    "player_position": player.player_position,
    "player_dead": player.player_dead,
    "player_isHost": player.player_isHost
    }


@router.delete("/players/{player_id}")
async def delete_player(player_id: int) :
    with db_session:
        try:
            fetch_player = get_jugador(player_id)
            db_player[player_id].delete()
        except ObjectNotFound:
            message = "El jugador no existe"
            status_code = 404 # not found
            return JSONResponse(content=message, status_code=status_code)
    message = "Jugador borrado!"
    status_code = 200 # no acceptable
    return JSONResponse(content=message, status_code=status_code)



# @router.get("/lobbys/list")
# async def lista_lobbys() -> List[ListedLobbys]:
#     listed_lobby = []
#     with db_session:
#         lobbys = list(db_lobby.select(lambda p: p.lobby_id > 0))
#         for c in lobbys:
#             lobby_info = Buscar_Lobby(c.lobby_id)
#             listed_lobby.append(lobby_info)
#         return listed_lobby