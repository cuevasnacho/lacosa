from pydantic import *

class Lobby(BaseModel):
    id : int
    name: str
    max : int
    min : int


class Card(BaseModel):
    id: int