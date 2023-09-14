# antes de empezar necesitamos descargar fastAPI, lo hacemos usando el siguiente comando
#pip install "fastapi[all]"


from fastapi import FastAPI

app = FastAPI()

@app.get("/")
# Un decorador en Python es una función especial que se utiliza para modificar o extender el comportamiento de otra función o método sin cambiar su código fuente
# estamos haciendo un get de la app para cargar la pagina

async def root():   #nuestra app hace la peticion asincrona y mientras el servidor sigue operando sin esperar a que root termine, osea en segundo plano
    return "Hola gato"
    
@app.get("/url")  #aca definimos un path para nuestro servidor entonces si agregamos al final /url a nuestro navegador, obtenemos la pagina con tal path
async def url():   
    return {"messi":"EL MEJOR DEL MUNDO"}

# ahora si a partir de nuestra url ponemos al final /docs, ingresaremos a la documentacion oficial generada por swagger


#para poder correr el servidor, usamos el comando 
#uvicorn main:app --reload
#diccionario: uvicorn (programa para levantar el server)
#main:app (usamos el archivo main.py y usamos la funcion app)
#--reload (esto va a recargar el servidor a por cada minimo cambio que hagamos en el archivo, recomiendo ctrl+c si estamos implementando cosas grandes para que no te explote la CPU)