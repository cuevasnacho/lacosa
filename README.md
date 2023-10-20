# La Cosa
## Ingenieria del Software I

### Integrantes

Nombre y Apellido | Usuario Github | Mail Jira

- Bruno Volpini, Volomeg23, bruno.volpini@mi.unc.edu.ar
- Marcos Delhugo, MarcosDelhugo, marcos.delhugo@mi.unc.edu.ar
- Marcos Strasorier, marcosstrasorier, marcos.strasorier@mi.unc.edu.ar
- Ignacio Ramirez, irmrz, ignaciotramirez@mi.unc.edu.ar
- Ignacio Cuevas, cuevasnacho, icuevas@mi.unc.edu.ar
- Tomas Marmay, tmarmay, tomas.marmay@mi.unc.edu.ar
- Tomas Hubmann, HubmannTomasAlejandro, tomas.hubmann@mi.unc.edu.ar

#### Primer Sprint
Product Owner: Tomas Marmay  
SCRUM Master: Ignacio Cuevas

#### Segundo Sprint
Product Owner: Marcos Strasorier  
SCRUM Master: Ignacio Ramirez

#### Instalar dependecias 
- *backend* : `pip install -r requirements.txt`
- *frontend* : 
  - `sudo apt-get install -y ca-certificates curl gnupg`
  - `sudo mkdir -p /etc/apt/keyrings`
  - `curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg`
  - `NODE_MAJOR=20`
  - `echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list`
  - `sudo apt-get install nodejs -y`
  - `npm init vite` (en la carpeta anterior al proyecto)


#### Levantar servidor backend
`uvicorn main:app --reload`

#### Levantar servidor frontend
`npm run dev`

#### Documentacion
[Endpoints](https://docs.google.com/spreadsheets/d/1iZtmSpPk-RzkIFN44DFs4zCZbBf5Tnz-C51Uslvtea4/edit#gid=0)  
[Descricion de tareas](https://docs.google.com/document/d/1yaT5ehNTlyQsrAsdwD0wDjCCZYnnLdfWiQRghbaUVJ8/edit?usp=sharing)  
[Front-End](https://docs.google.com/document/d/1eWJquCqwPrM_vrPEykkix5NLm3n92V1xVEOsFFc3wcE/edit?usp=sharing)  
[Preguntas Pertinentes](https://docs.google.com/document/d/1fX02lkKujGKvnqRw1EOlAYpgrj5wy6cFJQEnu2aq5cY/edit)  
[FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/)

#### Formato branches: SCRUM-(numeroticket)_Titulo#Descripcion
