# IAVE Landing page
IAVE - Landing page para o servidor offline


Esta ferramenta serve para facilitar a utilização do servidor offline do iave.
Em vez de fornecer o endereço do servidor offline (ip+porta), é fornecido o IP desta landing page. Ao fim de alguns segundos, é redirecionado para o endereço ip do servidor do iave.

Para além de servir de landing page, serve também para download dos ficheiros .exe|.dmg|.AppImage o que poderá ser mais rápido em caso de sobrecarga dos servidores officiais.



Como correr esta app usando **docker**.

# Etapa 1: Clonar 
Clonar este repositório e entrar nessa pasta.
```bash
git clone https://github.com/jpedrodias/IAVE_Landing_page.git
cd IAVE_Landing_page
```


# Etapa 2: Definir variáveis de ambiente 
Alterar valores das variáveis de ambiente no ficheiro `.env`:
```bash
nano .env
```

 - `FLASKAPP_REDIRECT_URL` - endereço do servidor do iave
 - `FLASKAPP_TITLE` - título que irá aparecer na página de loading



# Etapa 3: Download das aplicações oficiais
Fazer download dos ficheiros executáveis do site official e colocar na pasta `flaskapp/download`:


```bash
wget -P flaskapp/download https://assets.iave.pt/production/apps/intuitivo-app/v0.0.11/Provas+IAVE-0.0.11.exe

wget -P flaskapp/download https://assets.iave.pt/production/apps/intuitivo-app/v0.0.11/Provas+IAVE-0.0.11.dmg

wget -P flaskapp/download https://assets.iave.pt/production/apps/intuitivo-app/v0.0.11/Provas+IAVE-0.0.11.AppImage

```


# Etapa 4: Go Live

DRY RUN: verificar se está tudo bem. O primeiro arranque é demorado pois será feito o download do postgres e do python. Uma imagem para correr a aplicação flask será preparada.

**Dry run:**
Correr o docker container com a instrução 
```bash
docker compose up
```

Depois do primeiro `dry-run`, testar o acesso através do ip da máquina onde é iniciada a aplicação. 

Interrumper com `ctrl+c` e voltar a correr em background

PS: Ponderar correr usando gunicorn (ver Avançado)
```bash
docker compose up -d
```


# Etapa 5: Fecho e limpeza total:
Se for necessário parar o docker container que esteja a correr em background 
```bash
docker compose down -v
```
As seguintes instruções limpam a cache do docker 

**Limpeza docker**
```bash
df -h
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q) -f
docker volume rm $(docker volume ls -q)
docker network prune -f
docker system prune -a --volumes -f
df -h
```




---
**Avançado:**

- editar o ficheiro `docker-compose.yml`:
  alterar `command` para usar `gunicorn` mas só depois do primeiro arranque. No primeiro arranque, deixar em `python`


- `/views` listará todos os dispositivos que usaram a landing page. E é ainda possível fazer downlaod dessa listagem no formato `.csv` 


- para correr **com extras** fazer 
```bash
docker compose -f docker-compose_with_extras.yml up
```
---
