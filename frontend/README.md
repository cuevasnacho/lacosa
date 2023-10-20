# LaCosa FrontEnd

### Integrantes
Nombre y Apellido | Usuario Github | Mail Jira
- Ignacio Cuevas, cuevasnacho, icuevas@mi.unc.edu.ar
- Marcos Delhugo, MarcosDelhugo, marcos.delhugo@mi.unc.edu.ar
- Ignacio Ramirez, irmrz, ignaciotramirez@mi.unc.edu.ar

## Dependencias
### Node
Las instrucciones oficiales estan en [este link](https://github.com/nodesource/distributions#installation-instructions)

1. Download and import the Nodesource GPG key
```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
```
2. Create deb repository
```bash
NODE_MAJOR=20
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
```
3. Run Update and Install
```bash
sudo apt-get update
sudo apt-get install nodejs -y
```

### Fastapi-vite
Las instrucciones oficiales estan en [este link](https://pypi.org/project/fastapi-vite/)
```bash
pip install fastapi-vite
```

## Como Correr el proyecto
Para ejecutar el frontend de La Cosa desde el directorio raíz:

1. Enter frontend directory
```bash
cd frontend/
```

2. Install dependencies
```bash
npm install
```

3. Run frontend
```bash
npm run dev
```