#levantar el servidor 
#uvicorn main:app --reload

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

#configuro directorio de archivos estaticos 
app.mount("/static", StaticFiles(directory="static"), name="static")

#configuro directorio de paginas dinamicas
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


#hace pattern maching entra en el primero
@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]
@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]



